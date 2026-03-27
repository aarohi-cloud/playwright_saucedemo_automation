"""
Email reporter — sends a test-results email after the pytest session ends.
Activated only when EMAIL_ENABLED=true in the environment (or .env file).
"""
import os
import smtplib
import zipfile
from dataclasses import dataclass, field
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List


@dataclass
class EmailConfig:
    enabled: bool = field(default_factory=lambda: os.getenv("EMAIL_ENABLED", "false").lower() == "true")
    smtp_host: str = field(default_factory=lambda: os.getenv("SMTP_HOST", "smtp.gmail.com"))
    smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "587")))
    username: str = field(default_factory=lambda: os.getenv("SMTP_USERNAME", ""))
    password: str = field(default_factory=lambda: os.getenv("SMTP_PASSWORD", ""))
    email_from: str = field(default_factory=lambda: os.getenv("EMAIL_FROM", ""))
    email_to: str = field(default_factory=lambda: os.getenv("EMAIL_TO", ""))
    use_tls: bool = field(default_factory=lambda: os.getenv("EMAIL_USE_TLS", "true").lower() == "true")
    subject_prefix: str = field(default_factory=lambda: os.getenv("EMAIL_SUBJECT_PREFIX", "SauceDemo Tests"))


def _parse_junit_xml(xml_path: Path):
    """Parse junit XML and return (tests, failures, errors, skipped, failed_names)."""
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Handle both <testsuites> and <testsuite> root elements
        suite = root if root.tag == "testsuite" else root.find("testsuite")
        if suite is None:
            suite = root

        tests = int(suite.get("tests", 0))
        failures = int(suite.get("failures", 0))
        errors = int(suite.get("errors", 0))
        skipped = int(suite.get("skipped", 0))

        failed_names: List[str] = []
        for tc in suite.iter("testcase"):
            if tc.find("failure") is not None or tc.find("error") is not None:
                classname = tc.get("classname", "")
                name = tc.get("name", "")
                failed_names.append(f"{classname}::{name}" if classname else name)

        return tests, failures + errors, skipped, failed_names
    except Exception as exc:
        print(f"[email_reporter] Could not parse junit XML: {exc}")
        return 0, 0, 0, []


def _zip_reports(zip_path: Path) -> None:
    """Zip html and junit reports into a single archive."""
    reports_dir = Path("reports")
    html_report = reports_dir / "report.html"
    junit_report = reports_dir / "junit-report.xml"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        if html_report.exists():
            zf.write(html_report, html_report.name)
        if junit_report.exists():
            zf.write(junit_report, junit_report.name)


def send_email_report(exitstatus: int) -> None:
    """Send email with test results. Does nothing if EMAIL_ENABLED != 'true'."""
    cfg = EmailConfig()

    if not cfg.enabled:
        return

    try:
        junit_path = Path("reports") / "junit-report.xml"
        tests, failed, skipped, failed_names = _parse_junit_xml(junit_path)
        passed = tests - failed - skipped

        status_label = "PASSED" if failed == 0 else "FAILED"
        subject = f"{cfg.subject_prefix} — {status_label} ({passed}/{tests})"

        # Build body
        lines = [
            f"Test run finished with exit status: {exitstatus}",
            f"",
            f"Results:",
            f"  Total  : {tests}",
            f"  Passed : {passed}",
            f"  Failed : {failed}",
            f"  Skipped: {skipped}",
        ]

        if failed_names:
            lines += ["", "Failed tests (up to 5):"]
            for name in failed_names[:5]:
                lines.append(f"  - {name}")

        body = "\n".join(lines)

        # Build message
        msg = MIMEMultipart()
        msg["From"] = cfg.email_from
        msg["To"] = cfg.email_to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Attach zip of reports
        zip_path = Path("reports") / "test-reports.zip"
        try:
            _zip_reports(zip_path)
            if zip_path.exists():
                with open(zip_path, "rb") as f:
                    part = MIMEBase("application", "zip")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{zip_path.name}"')
                msg.attach(part)
        except Exception as exc:
            print(f"[email_reporter] Could not attach reports zip: {exc}")

        # Send
        with smtplib.SMTP(cfg.smtp_host, cfg.smtp_port) as server:
            if cfg.use_tls:
                server.starttls()
            if cfg.username and cfg.password:
                server.login(cfg.username, cfg.password)
            server.sendmail(cfg.email_from, cfg.email_to, msg.as_string())

        print(f"[email_reporter] Report sent to: {cfg.email_to}")

    except Exception as exc:
        print(f"[email_reporter] Failed to send report: {exc}")

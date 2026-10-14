import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from pathlib import Path
from flask import current_app

logger = logging.getLogger('portfolio.email_service')


class EmailService:
    """Handles notification delivery with resilient SMTP dispatch and safe file logging."""

    @classmethod
    def send_inquiry(cls, name: str, email: str, subject: str, message: str, ip_address: str = "unknown") -> bool:
        """Sends an inquiry notification to Jayaprakash Biswal or logs to fallback storage."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        recipient = current_app.config.get('CONTACT_RECIPIENT_EMAIL', 'jayprakashbiswa49@gmail.com')

        # Check if SMTP configuration is present
        server = current_app.config.get('MAIL_SERVER')
        username = current_app.config.get('MAIL_USERNAME')
        password = current_app.config.get('MAIL_PASSWORD')
        port = current_app.config.get('MAIL_PORT', 587)
        use_tls = current_app.config.get('MAIL_USE_TLS', True)

        if server and username and password:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f"[Portfolio Contact] {subject} - from {name}"
                msg['From'] = current_app.config.get('MAIL_DEFAULT_SENDER', username)
                msg['To'] = recipient
                msg['Reply-To'] = email

                plain_body = (
                    f"New message submitted via Developer Portfolio:\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Subject: {subject}\n"
                    f"Timestamp: {timestamp}\n"
                    f"IP Address: {ip_address}\n\n"
                    f"Message:\n{message}\n"
                )
                msg.attach(MIMEText(plain_body, 'plain', 'utf-8'))

                # Connect and send
                smtp = smtplib.SMTP(server, port, timeout=10)
                if use_tls:
                    smtp.starttls()
                smtp.login(username, password)
                smtp.sendmail(msg['From'], [recipient], msg.as_string())
                smtp.quit()

                logger.info(f"Inquiry successfully delivered via SMTP to {recipient} from {email}")
                cls._log_to_file(name, email, subject, message, timestamp, ip_address, status="DELIVERED_SMTP")
                return True
            except Exception as e:
                logger.error(f"SMTP dispatch failed: {e}. Falling back to persistent log.")
                cls._log_to_file(name, email, subject, message, timestamp, ip_address, status="SMTP_FAILED_LOGGED")
                return True
        else:
            # SMTP not configured: save securely to fallback logger
            logger.info("SMTP not configured in environment. Persisting inquiry to application storage.")
            cls._log_to_file(name, email, subject, message, timestamp, ip_address, status="PERSISTED_OFFLINE")
            return True

    @classmethod
    def _log_to_file(cls, name: str, email: str, subject: str, message: str,
                     timestamp: str, ip_address: str, status: str) -> None:
        """Appends inquiry data to logs/inquiries.log with defensive error handling."""
        try:
            logs_dir = Path(current_app.root_path).parent / "logs"
            logs_dir.mkdir(exist_ok=True)
            log_file = logs_dir / "inquiries.log"

            entry = (
                f"\n--- [{timestamp}] Status: {status} ---\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Subject: {subject}\n"
                f"IP: {ip_address}\n"
                f"Message:\n{message}\n"
                f"{'='*60}\n"
            )

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            logger.error(f"Failed to append to inquiries.log: {e}")

# src/infrastructure/email/email_service.py
import smtplib
from email.mime.text import MIMEText
from config.setting import settings

class EmailService:
    def send_email(self, to_email: str, subject: str, body: str):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_USER
        msg['To'] = to_email

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_USER, [to_email], msg.as_string())
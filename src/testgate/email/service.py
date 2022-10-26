import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from src.testgate.email.constants import SMTP_EMAIL_ADDRESS, SMTP_EMAIL_APP_PASSWORD


class EmailService:

    def __init__(self):
        self._email_subject: Optional[str] = None
        self._email_from: Optional[str] = None
        self._email_to: Optional[str] = None
        self._email_messages: Optional[MIMEMultipart] = MIMEMultipart('alternative')
        self._email_password: Optional[str] = None
        self._smtp_server: Optional[smtplib.SMTP] = None

    @property
    def email_subject(self) -> str:
        return self._email_subject

    @email_subject.setter
    def email_subject(self, value: str):
        self._email_subject = value

    @property
    def email_from(self) -> str:
        return self._email_from

    @email_from.setter
    def email_from(self, value: str):
        self._email_from = value

    @property
    def email_to(self) -> str:
        return self._email_to

    @email_to.setter
    def email_to(self, value: str):
        self._email_to = value

    @property
    def email_messages(self) -> MIMEMultipart:
        return self._email_messages

    @email_messages.setter
    def email_messages(self, value):
        self._email_messages = value

    @property
    def email_password(self) -> str:
        return self._email_password

    @email_password.setter
    def email_password(self, value):
        self._email_password = value

    def add_plain_text_message(self, plain_text: str):
        message = MIMEText(plain_text, 'plain')
        self._email_messages.attach(message)

    def add_html_message(self, html: str):
        message = MIMEText(html, 'html')
        self._email_messages.attach(message)

    def start_smtp_server(self):
        self._smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        self._smtp_server.ehlo()
        self._smtp_server.starttls()
        self._smtp_server.login(self._email_from, self._email_password)

    def send_email(self):
        self._email_messages['Subject'] = self._email_subject
        self._email_messages['From'] = self._email_from
        self._email_messages['To'] = self.email_to
        self._smtp_server.sendmail(self.email_from, self._email_to, self._email_messages.as_string())
        self._smtp_server.quit()


def get_email_service():
    email_service = EmailService()
    email_service.email_from = SMTP_EMAIL_ADDRESS
    email_service.email_password = SMTP_EMAIL_APP_PASSWORD
    email_service.start_smtp_server()
    return email_service

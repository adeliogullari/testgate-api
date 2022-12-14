import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Tuple, List


class EmailService:

    def __init__(self):
        self._email_subject: Optional[str] = None
        self._email_from: Optional[str] = None
        self._email_to: Optional[str] = None
        self._email_messages: Optional[MIMEMultipart] = MIMEMultipart('alternative')
        self._email_password: Optional[str] = None

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

    def send_email(self):
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(self._email_from, self._email_password)

        self._email_messages['Subject'] = self._email_subject
        self._email_messages['From'] = self._email_from
        self._email_messages['To'] = self.email_to

        smtp_server.sendmail(self.email_from, self._email_to, self._email_messages.as_string())
        smtp_server.quit()

from smtplib import SMTP
from config import Settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

settings = Settings()


class EmailService:
    def __init__(self) -> None:
        self._email_subject: str = ""
        self._email_from: str = ""
        self._email_to: str = ""
        self._email_password: str = ""
        self._email_messages: MIMEMultipart = MIMEMultipart("alternative")
        self._smtp_server: SMTP = SMTP("smtp.gmail.com", 587)

    @property
    def email_subject(self) -> str | None:
        return self._email_subject

    @email_subject.setter
    def email_subject(self, value: str) -> None:
        self._email_subject = value

    @property
    def email_from(self) -> str:
        return self._email_from

    @email_from.setter
    def email_from(self, value: str) -> None:
        self._email_from = value

    @property
    def email_to(self) -> str | None:
        return self._email_to

    @email_to.setter
    def email_to(self, value: str) -> None:
        self._email_to = value

    @property
    def email_messages(self) -> MIMEMultipart:
        return self._email_messages

    @email_messages.setter
    def email_messages(self, value: MIMEMultipart) -> None:
        self._email_messages = value

    @property
    def email_password(self) -> str | None:
        return self._email_password

    @email_password.setter
    def email_password(self, value: str) -> None:
        self._email_password = value

    @property
    def smtp_server(self) -> SMTP | None:
        return self._smtp_server

    @smtp_server.setter
    def smtp_server(self, value: SMTP) -> None:
        self._smtp_server = value

    def add_plain_text_message(self, plain_text: str) -> None:
        message = MIMEText(plain_text, "plain")
        self._email_messages.attach(message)

    def add_html_message(self, html: str) -> None:
        message = MIMEText(html, "html")
        self._email_messages.attach(message)

    def start_smtp_server(self) -> None:
        self._smtp_server.ehlo()
        self._smtp_server.starttls()
        self._smtp_server.login(self._email_from, self._email_password)

    def send_email(self) -> None:
        self._email_messages["Subject"] = self._email_subject
        self._email_messages["From"] = self._email_from
        self._email_messages["To"] = self.email_to
        self._smtp_server.sendmail(
            self.email_from, self._email_to, self._email_messages.as_string()
        )
        # self._smtp_server.quit()


def get_email_service() -> EmailService:
    email_service = EmailService()
    email_service.email_from = settings.testgate_smtp_email_address
    email_service.email_password = settings.testgate_smtp_email_app_password
    email_service.start_smtp_server()
    return email_service


async def email_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("email", b"Super message")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


async def email_consumer():
    consumer = AIOKafkaConsumer(
        'email',
        bootstrap_servers='localhost:9092',
        group_id="email")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
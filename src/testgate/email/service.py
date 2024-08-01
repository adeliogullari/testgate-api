from typing import Any, Sequence
from smtplib import SMTP
from config import Settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.testgate.kafka.service import aio_kafka_producer, aio_kafka_consumer

settings = Settings()


class EmailService:
    def __init__(self, host: str, port: int) -> None:
        self._mime_message: MIMEMultipart = MIMEMultipart("alternative")
        self._smtp_server: SMTP = SMTP(host=host, port=port)

    @property
    def mime_message(self) -> MIMEMultipart:
        return self._mime_message

    @mime_message.setter
    def mime_message(self, value: MIMEMultipart) -> None:
        self._mime_message = value

    @property
    def smtp_server(self) -> SMTP:
        return self._smtp_server

    @smtp_server.setter
    def smtp_server(self, value: SMTP) -> None:
        self._smtp_server = value

    def add_subject(self, subject: str) -> None:
        self.mime_message["Subject"] = subject

    def add_plain_text_message(self, plain_text: str) -> None:
        message = MIMEText(plain_text, "plain")
        self.mime_message.attach(message)

    def add_html_message(self, html: str) -> None:
        message = MIMEText(html, "html")
        self.mime_message.attach(message)

    def login_smtp_server(self, username: str, password: str) -> None:
        self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.login(user=username, password=password)

    def send_email(self, from_addr: str, to_addrs: str | Sequence[str]) -> None:
        self.smtp_server.sendmail(
            from_addr=from_addr, to_addrs=to_addrs, msg=self.mime_message.as_string()
        )


async def aio_kafka_email_producer(value: Any) -> None:
    producer = await aio_kafka_producer()
    await producer.start()
    try:
        await producer.send_and_wait(topic="email", value=value)
    finally:
        await producer.stop()


async def aio_kafka_email_consumer() -> None:
    consumer = await aio_kafka_consumer()
    consumer.subscribe(topics=["email"])

    await consumer.start()
    try:
        async for msg in consumer:
            email_service = EmailService(
                host=settings.testgate_smtp_email_host,
                port=settings.testgate_smtp_email_port,
            )
            email_service.add_subject(msg.value["subject"])
            email_service.add_plain_text_message(msg.value["plain_text_message"])
            email_service.add_html_message(msg.value["html_message"])
            email_service.login_smtp_server(
                username=settings.testgate_smtp_email_username,
                password=settings.testgate_smtp_email_password,
            )
            email_service.send_email(
                from_addr=settings.testgate_smtp_email_address,
                to_addrs=msg.value["to_addrs"],
            )
    finally:
        await consumer.stop()

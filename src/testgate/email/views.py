import asyncio

from sqlmodel import Session
from fastapi import APIRouter, Depends
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from src.testgate.email.schema import SendEmailModel

from config import get_settings, Settings

from src.testgate.email.service import EmailService, get_email_service, email_producer, email_consumer, aio_kafka_email_producer
from src.testgate.database.service import get_session
from src.testgate.kafka.service import aio_kafka_producer, aio_kafka_consumer

router = APIRouter(tags=["email"])


@router.post(path="/api/v1/email", response_model=None, status_code=200)
def send_email(
    *,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
    email: SendEmailModel,
    email_service: EmailService = Depends(get_email_service),
):
    email_service.email_subject = email.subject
    email_service.email_from = settings.testgate_smtp_email_address
    email_service.email_password = settings.testgate_smtp_email_app_password
    email_service.email_to = email.to_address
    email_service.add_plain_text_message(email.plain_text_message)
    email_service.add_html_message(email.html_message)
    email_service.send_email()


@router.post(path="/api/v1/email_kafka", response_model=None, status_code=200)
async def send_email_kafka(
    *,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
    email: SendEmailModel,
    email_service: EmailService = Depends(get_email_service),
):
    response = await aio_kafka_email_producer(value=email.model_dump())
    return response
    # await email_producer()
    # response = await aio_kafka_producer(topic="email", value=email)
    # return response

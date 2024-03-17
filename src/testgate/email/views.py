from sqlmodel import Session
from fastapi import APIRouter, Depends
from src.testgate.email.schema import SendEmailModel
from src.testgate.email.service import (
    EmailService,
    aio_kafka_email_producer,
)
from src.testgate.database.service import get_sqlmodel_session, get_redis_client

router = APIRouter(tags=["emails"])


@router.post(path="/api/v1/emails", response_model=None, status_code=200)
async def send_email(
    *,
    email: SendEmailModel,
):
    await aio_kafka_email_producer(value=email.model_dump())
    return email

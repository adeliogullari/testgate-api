from fastapi import APIRouter
from src.testgate.email.schema import SendEmailModel
from src.testgate.email.service import (
    aio_kafka_email_producer,
)

router = APIRouter(tags=["emails"])


@router.post(path="/api/v1/emails", response_model=None, status_code=200)
async def send_email(
    *,
    email: SendEmailModel,
):
    await aio_kafka_email_producer(value=email.model_dump())
    return email

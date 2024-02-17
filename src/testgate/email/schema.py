from sqlmodel import SQLModel
from typing import Any


class SendEmailModel(SQLModel):
    subject: str
    to_address: str
    plain_text_message: str
    html_message: str

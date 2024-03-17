from sqlmodel import SQLModel


class SendEmailModel(SQLModel):
    subject: str
    to_addrs: str | list[str]
    plain_text_message: str
    html_message: str


class SendEmailProducerModel(SQLModel):
    subject: str
    to_addrs: str | list[str]
    plain_text_message: str
    html_message: str

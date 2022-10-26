from typing import Optional, Any
from sqlmodel import SQLModel
from pydantic import validator
from bcrypt import hashpw, gensalt
from jose import jwt
from datetime import datetime
from datetime import timedelta


class AuthLoginRequestModel(SQLModel):
    email: Optional[Any]
    password: Optional[Any]


class AuthLoginResponseModel(SQLModel):
    email: Optional[str]
    # token: Optional[str]
    #
    # @validator('token', pre=True, always=True)
    # def generate_token(cls, v, values, **kwargs):
    #     return "token"


class AuthRegisterRequestModel(SQLModel):
    firstname: str
    lastname: str
    email: str
    password: str


class AuthRegisterResponseModel(SQLModel):
    firstname: str
    lastname: str
    email: str
    password: str


# class AuthenticateUserRequestModel(SQLModel):
#     email: str
#     password: str
#
#
# class AuthenticateUserResponseModel(SQLModel):
#     id: str
#     token: Optional[str]
#
#     @validator('token', pre=True, always=True)
#     def generate_token(cls, v, values, **kwargs):
#         now = datetime.utcnow()
#         exp = (now + timedelta(seconds=JWT_TOKEN_EXP)).timestamp()
#         email = values.get("email")
#         claims = {"exp": exp, "email": email}
#         return jwt.encode(claims=claims, key=JWT_TOKEN_KEY, algorithm=JWT_TOKEN_ALGORITHM)
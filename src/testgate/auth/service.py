from typing import Optional
from sqlmodel import Session
from .schemas import RegisterCredentials
from src.testgate.user.models import User


def register(*, session: Session, credentials: RegisterCredentials) -> Optional[User]:
    """Register a new user."""

    created_user = User()
    created_user.firstname = credentials.firstname
    created_user.lastname = credentials.lastname
    created_user.username = credentials.username
    created_user.email = credentials.email
    created_user.password = credentials.password

    session.add(created_user)
    session.commit()
    session.refresh(created_user)

    return created_user

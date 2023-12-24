from typing import Optional
from sqlmodel import Session
from src.testgate.user.models import User
from src.testgate.auth.schemas import RegisterCredentials


def register(*, session: Session, credentials: RegisterCredentials) -> Optional[User]:
    """Registers a new user."""

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

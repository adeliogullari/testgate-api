from sqlmodel import Session
from src.testgate.user.models import User
from src.testgate.auth.schemas import RegisterCredentials


def register(*, session: Session, credentials: RegisterCredentials) -> User:
    """Registers a new user."""

    created_user = User(
        firstname=credentials.firstname,
        lastname=credentials.lastname,
        username=credentials.username,
        email=credentials.email,
        password=credentials.password,
    )

    session.add(created_user)
    session.commit()
    session.refresh(created_user)

    return created_user

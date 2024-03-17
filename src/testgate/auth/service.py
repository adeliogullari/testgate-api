from sqlmodel import Session
from src.testgate.user.models import User
from src.testgate.auth.schemas import RegisterCredentials


async def register(
    *, sqlmodel_session: Session, credentials: RegisterCredentials
) -> User:
    """Registers a new user."""

    created_user = User(
        firstname=credentials.firstname,
        lastname=credentials.lastname,
        username=credentials.username,
        email=credentials.email,
        password=credentials.password,
    )

    sqlmodel_session.add(created_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_user)

    return created_user

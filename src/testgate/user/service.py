from typing import Any, Sequence
from sqlmodel import select, Session
from src.testgate.user.models import User
from src.testgate.user.schemas import (
    UserQueryParametersModel,
    CreateUserRequestModel,
    UpdateUserRequestModel,
)
from src.testgate.role.models import Role


async def retrieve_by_id(*, sqlmodel_session: Session, user_id: int) -> User:
    """Returns a user object based on the given user id."""

    statement: Any = select(User).where(User.id == user_id)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_username(
    *, sqlmodel_session: Session, user_username: str
) -> User:
    """Returns a user object based on the given user username."""

    statement: Any = select(User).where(User.username == user_username)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_email(*, sqlmodel_session: Session, user_email: str) -> User:
    """Returns a user object based on the given user email."""

    statement: Any = select(User).where(User.email == user_email)

    retrieved_user = sqlmodel_session.exec(statement).one_or_none()

    return retrieved_user


async def retrieve_by_query_parameters(
    *, sqlmodel_session: Session, query_parameters: UserQueryParametersModel
) -> Sequence[User]:
    """Returns a user object based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(User).join(Role).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit"}, exclude_none=True
    ).items():
        statement = statement.where(getattr(User, attr) == value)

    retrieved_user = sqlmodel_session.exec(statement).all()

    return retrieved_user


async def create(*, sqlmodel_session: Session, user: CreateUserRequestModel) -> User:
    """Creates a new user."""

    created_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        password=user.password,
        verified=user.verified,
        image=user.image,
        role=user.role,
    )

    sqlmodel_session.add(created_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(created_user)

    return created_user


async def update(
    *, sqlmodel_session: Session, retrieved_user: User, user: UpdateUserRequestModel
) -> User:
    """Updates an existing user."""

    retrieved_user.firstname = user.firstname
    retrieved_user.lastname = user.lastname
    retrieved_user.email = user.email
    retrieved_user.verified = user.verified
    retrieved_user.image = user.image
    retrieved_user.role = user.role

    updated_user = retrieved_user

    sqlmodel_session.add(updated_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_user)

    return updated_user


async def update_password(
    *, sqlmodel_session: Session, retrieved_user: User, password: str
) -> User:
    """Updates an existing password"""

    retrieved_user.password = password

    updated_user = retrieved_user

    sqlmodel_session.add(updated_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(updated_user)

    return updated_user


async def verify(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    """Verifies an existing user."""

    retrieved_user.verified = True

    verified_user = retrieved_user

    sqlmodel_session.add(verified_user)
    sqlmodel_session.commit()
    sqlmodel_session.refresh(verified_user)

    return verified_user


async def delete(*, sqlmodel_session: Session, retrieved_user: User) -> User:
    """Deletes an existing user."""

    sqlmodel_session.delete(retrieved_user)
    sqlmodel_session.commit()

    return retrieved_user

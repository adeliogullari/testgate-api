from typing import Optional, List
from sqlmodel import select, Session
from src.testgate.user.models import User
from src.testgate.user.schemas import (
    UserQueryParametersModel,
    CreateUserRequestModel,
    UpdateUserRequestModel,
)
from src.testgate.role.models import Role


def retrieve_by_id(*, session: Session, user_id: int) -> User | None:
    """Returns a user object based on the given user id."""

    statement = select(User).where(User.id == user_id)

    retrieved_user = session.exec(statement).one_or_none()

    return retrieved_user


def retrieve_by_username(*, session: Session, user_username: str) -> User | None:
    """Returns a user object based on the given user username."""

    statement = select(User).where(User.username == user_username)

    retrieved_user = session.exec(statement).one_or_none()

    return retrieved_user


def retrieve_by_email(*, session: Session, user_email: str) -> User | None:
    """Returns a user object based on the given user email."""

    statement = select(User).where(User.email == user_email)

    retrieved_user = session.exec(statement).one_or_none()

    return retrieved_user


def retrieve_by_query_parameters(
    *, session: Session, query_parameters: UserQueryParametersModel
) -> Optional[List[User]]:
    """Returns a user object based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement = select(User).join(Role).offset(offset).limit(limit)

    for attr, value in query_parameters.dict(
        exclude={"offset", "limit"}, exclude_none=True
    ).items():
        statement = statement.where(getattr(User, attr) == value)

    # statement = statement.where(Role.name == query_parameters.role)

    retrieved_user = session.exec(statement).all()

    return retrieved_user


def create(*, session: Session, user: CreateUserRequestModel) -> Optional[User]:
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

    session.add(created_user)
    session.commit()
    session.refresh(created_user)

    return created_user


def update(
    *, session: Session, retrieved_user: User, user: UpdateUserRequestModel
) -> Optional[User]:
    """Updates an existing user."""

    retrieved_user.firstname = user.firstname
    retrieved_user.lastname = user.lastname
    retrieved_user.email = user.email
    retrieved_user.verified = user.verified
    retrieved_user.image = user.image
    retrieved_user.role = user.role

    updated_user = retrieved_user

    session.add(updated_user)
    session.commit()
    session.refresh(updated_user)

    return updated_user


def update_password(
    *, session: Session, retrieved_user: User, password: str
) -> Optional[User]:
    """Updates an existing password"""

    retrieved_user.password = password

    updated_user = retrieved_user

    session.add(updated_user)
    session.commit()
    session.refresh(updated_user)

    return updated_user


def verify(*, session: Session, retrieved_user: User) -> User:
    """Verifies an existing user."""

    retrieved_user.verified = True

    verified_user = retrieved_user

    session.add(verified_user)
    session.commit()
    session.refresh(verified_user)

    return verified_user


def delete(*, session: Session, retrieved_user: User) -> Optional[User]:
    """Deletes an existing user."""

    session.delete(retrieved_user)
    session.commit()

    return retrieved_user

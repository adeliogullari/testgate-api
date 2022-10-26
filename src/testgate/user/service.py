from typing import Optional, List, Any
from sqlmodel import select, Session, col

from .models import User
from src.testgate.role.models import Role
from src.testgate.team.models import Team
from .schemas import UserQueryParametersModel,\
                     CreateUserRequestModel, \
                     UpdateUserRequestModel


def retrieve_by_id(*, session: Session, id: int) -> Optional[User]:
    """Returns a user object based on the given user id."""

    statement = select(User).where(User.id == id)

    retrieved_user = session.exec(statement).one_or_none()

    return retrieved_user


def retrieve_by_email(*, session: Session, email: str) -> Optional[User]:
    """Returns a user object based on the given user email."""

    statement = select(User).where(User.email == email)

    retrieved_user = session.exec(statement).one_or_none()

    return retrieved_user


def retrieve_by_query_parameters(*, session: Session, query_parameters: UserQueryParametersModel) -> Optional[List[User]]:
    """Returns a user object based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement = select(User).join(Role).join(Team).offset(offset).limit(limit)

    for attr, value in query_parameters.dict(exclude={'role', 'team'}, exclude_none=True).items():
        statement = statement.where(getattr(User, attr) == value)

    statement = statement.where(Role.name == query_parameters.role)
    statement = statement.where(Team.name == query_parameters.team)

    retrieved_user = session.exec(statement).all()

    return retrieved_user


def create(*, session: Session, user: CreateUserRequestModel) -> Optional[User]:
    """Creates a new user."""

    created_user = User()
    created_user.firstname = user.firstname
    created_user.lastname = user.lastname
    created_user.email = user.email
    created_user.password = user.password
    created_user.verified = user.verified
    created_user.image = user.image
    created_user.role = user.role
    created_user.team = user.team

    session.add(created_user)
    session.commit()
    session.refresh(created_user)

    return created_user


def update(*, session: Session, retrieved_user: User, user: UpdateUserRequestModel) -> Optional[User]:
    """Updates an existing user."""

    retrieved_user.firstname = user.firstname
    retrieved_user.lastname = user.lastname
    retrieved_user.email = user.email
    retrieved_user.verified = user.verified
    retrieved_user.image = user.image
    retrieved_user.role = user.role
    retrieved_user.team = user.team

    updated_user = retrieved_user

    session.add(updated_user)
    session.commit()
    session.refresh(updated_user)

    return updated_user


def update_password(*, session: Session, retrieved_user: User, password: str) -> Optional[User]:
    """Updates an existing password"""

    retrieved_user.password = password

    updated_user = retrieved_user

    session.add(updated_user)
    session.commit()
    session.refresh(updated_user)

    return updated_user


def verify(*, session: Session, retrieved_user: User) -> Optional[User]:
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

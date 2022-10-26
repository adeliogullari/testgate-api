from typing import Optional, List
from sqlmodel import select, Session, col

from .models import User
from .schemas import SearchUserQueryParametersModel, \
                     CreateUserRequestModel, \
                     UpdateUserRequestModel
from .constants import *


def retrieve_user_by_id_service(*, session: Session, id: int) -> Optional[User]:
    """Returns a user object based on the given user id."""

    statement = select(User).where(User.id == id)

    retrieved_user = session.exec(statement).one_or_none()

    return retrieved_user


def retrieve_user_by_email_service(*, session: Session, email: str) -> Optional[User]:
    """Returns a user object based on the given user email."""

    statement = select(User).where(User.email == email)

    retrieved_user = session.exec(statement).one_or_none()

    return retrieved_user


def search_user_service(*, session: Session, query_parameters: SearchUserQueryParametersModel) -> Optional[List[User]]:
    """Returns a user object based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement = select(User).offset(offset).limit(limit)

    query_filter = ['firstname', 'lastname', 'email']
    filtered_query_parameters = {k: v for k, v in query_parameters.dict().items() if k in query_filter}

    for attr, value in filtered_query_parameters.items():
        if value:
            statement = statement.where(getattr(User, attr) == value)

    roles = query_parameters.roles

    for role in roles:
        statement = statement.where(col(User.roles).contains(role))

    teams = query_parameters.teams

    for team in teams:
        statement = statement.where(col(User.teams).contains(team))

    searched_user = session.exec(statement).all()

    return searched_user


def create_user_service(*, session: Session, user: CreateUserRequestModel) -> Optional[User]:
    """Creates a new user."""

    created_user = User()
    created_user.firstname = user.firstname
    created_user.lastname = user.lastname
    created_user.email = user.email
    created_user.password = user.password
    created_user.verified = user.verified
    created_user.roles = user.roles
    created_user.teams = user.teams

    session.add(created_user)
    session.commit()
    session.refresh(created_user)

    return created_user


def update_user_service(*, session: Session, retrieved_user: User, user: UpdateUserRequestModel) -> Optional[User]:
    """Updates an existing user."""

    retrieved_user.firstname = user.firstname
    retrieved_user.lastname = user.lastname
    retrieved_user.email = user.email
    retrieved_user.verified = user.verified
    retrieved_user.roles = user.roles
    retrieved_user.teams = user.teams

    updated_user = retrieved_user

    session.add(updated_user)
    session.commit()
    session.refresh(updated_user)

    return updated_user


def upsert_user_service(*, session: Session, user: CreateUserRequestModel) -> Optional[User]:
    """Upserts a new user."""

    retrieved_user = retrieve_user_by_email_service(session=session, email=user.email)

    if retrieved_user:
        return update_user_service(session=session, user=user)

    return create_user_service(session=session, user=user)


def delete_user_service(*, session: Session, retrieved_user: User) -> Optional[User]:
    """Deletes an existing user."""

    session.delete(retrieved_user)
    session.commit()

    return retrieved_user

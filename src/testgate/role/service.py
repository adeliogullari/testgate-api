from typing import Optional, List, Dict
from jose import jwt
from sqlmodel import select, Session

from ..role.models import Role
from ..team.models import Team

from .models import Role
from .schemas import RetrieveRoleResponseModel, CreateRoleRequestModel, DeleteRoleResponseModel, UpdateRoleRequestModel


def retrieve_role_by_id_service(*, session: Session, id: int) -> Optional[Role]:
    """Returns a role object based on the given role id."""

    statement = select(Role).where(Role.id == id)

    retrieved_role = session.exec(statement).one_or_none()

    return retrieved_role


def retrieve_role_by_name_service(*, session: Session, name: str) -> Optional[Role]:
    """Returns a role object based on the given role name."""

    statement = select(Role).where(Role.name == name)

    retrieved_role = session.exec(statement).one_or_none()

    return retrieved_role


def search_role_service(*, session: Session, query_parameters: dict) -> Optional[List[Role]]:
    """Returns a role object based on the given query parameters."""

    statement = select(Role)

    for attr, value in query_parameters.items():
        if value:
            statement = statement.filter(getattr(Role, attr).like(value))

    searched_role = session.exec(statement).all()

    return searched_role


def create_role_service(*, session: Session, role: CreateRoleRequestModel) -> Optional[Role]:
    """Creates a new role."""

    created_role = Role(**role.dict())

    session.add(created_role)
    session.commit()
    session.refresh(created_role)

    return created_role


def upsert_role_service(*, session: Session, role: CreateRoleRequestModel) -> Optional[Role]:
    """Upserts a new role"""

    retrieved_role = retrieve_role_by_name_service(session=session, name=role.name)

    if retrieved_role:
        return update_role_service(session=session, role=role)

    return create_role_service(session=session, role=role)


def update_role_service(*, session: Session, retrieved_role: Role, role: UpdateRoleRequestModel) -> Optional[Role]:
    """Updates an existing role."""

    retrieved_role.name = role.name
    updated_role = retrieved_role
    # for attr, value in role.dict().items():
    #     if value:
    #         setattr(retrieved_role, attr, value)
    #
    # updated_role = Role(**retrieved_role.dict())

    session.add(updated_role)
    session.commit()
    session.refresh(updated_role)

    return updated_role


def delete_role_by_id_service(*, session: Session, retrieved_role: Role) -> Optional[Role]:
    """Deletes an existing user."""

    session.delete(retrieved_role)
    session.commit()

    return retrieved_role

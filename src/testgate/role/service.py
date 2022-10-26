from typing import Optional, List
from sqlmodel import select, Session
from .models import Role
from .schemas import CreateRoleRequestModel, UpdateRoleRequestModel


def create(*, session: Session, role: CreateRoleRequestModel) -> Optional[Role]:
    """Creates a new role object."""

    created_role = Role()
    created_role.name = role.name

    session.add(created_role)
    session.commit()
    session.refresh(created_role)

    return created_role


def retrieve_by_id(*, session: Session, id: int) -> Optional[Role]:
    """Return a role object based on the given id."""

    statement = select(Role).where(Role.id == id)

    retrieved_role = session.exec(statement).one_or_none()

    return retrieved_role


def retrieve_by_name(*, session: Session, name: str) -> Optional[Role]:
    """Return a role object based on the given name."""

    statement = select(Role).where(Role.name == name)

    retrieved_role = session.exec(statement).one_or_none()

    return retrieved_role


def retrieve_by_query_parameters(*, session: Session, query_parameters: dict) -> Optional[List[Role]]:
    """Return list of role objects based on the given query parameters."""

    statement = select(Role)

    for attr, value in query_parameters.items():
        if value:
            statement = statement.filter(getattr(Role, attr).like(value))

    retrieved_roles = session.exec(statement).all()

    return retrieved_roles


def update(*, session: Session, retrieved_role: Role, role: UpdateRoleRequestModel) -> Optional[Role]:
    """Updates an existing role object."""

    retrieved_role.name = role.name
    updated_role = retrieved_role

    session.add(updated_role)
    session.commit()
    session.refresh(updated_role)

    return updated_role


def delete(*, session: Session, retrieved_role: Role) -> Optional[Role]:
    """Deletes an existing role object."""

    session.delete(retrieved_role)
    session.commit()

    return retrieved_role

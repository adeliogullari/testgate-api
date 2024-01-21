from typing import Any
from sqlmodel import select, Session
from .models import Role
from .schemas import CreateRoleRequestModel, RoleQueryParameters, UpdateRoleRequestModel


def create(*, session: Session, role: CreateRoleRequestModel) -> Role | None:
    """Creates a new role object."""

    created_role = Role()
    created_role.name = role.name

    session.add(created_role)
    session.commit()
    session.refresh(created_role)

    return created_role


def retrieve_by_id(*, session: Session, id: int) -> Role | None:
    """Return a role object based on the given id."""

    statement: Any = select(Role).where(Role.id == id)

    retrieved_role = session.exec(statement).one_or_none()

    return retrieved_role


def retrieve_by_name(*, session: Session, name: str) -> Role | None:
    """Return a role object based on the given name."""

    statement: Any = select(Role).where(Role.name == name)

    retrieved_role = session.exec(statement).one_or_none()

    return retrieved_role


def retrieve_by_query_parameters(
    *, session: Session, query_parameters: RoleQueryParameters
) -> list[Role] | None:
    """Return list of role objects based on the given query parameters."""

    offset = query_parameters.offset
    limit = query_parameters.limit

    statement: Any = select(Role).offset(offset).limit(limit)

    for attr, value in query_parameters.model_dump(
        exclude={"offset", "limit"}, exclude_none=True
    ).items():
        statement = statement.filter(getattr(Role, attr).like(value))

    retrieved_roles = session.exec(statement).all()

    return retrieved_roles


def update(
    *, session: Session, retrieved_role: Role, role: UpdateRoleRequestModel
) -> Role | None:
    """Updates an existing role object."""

    retrieved_role.name = role.name
    updated_role = retrieved_role

    session.add(updated_role)
    session.commit()
    session.refresh(updated_role)

    return updated_role


def delete(*, session: Session, retrieved_role: Role) -> Role | None:
    """Deletes an existing role object."""

    session.delete(retrieved_role)
    session.commit()

    return retrieved_role

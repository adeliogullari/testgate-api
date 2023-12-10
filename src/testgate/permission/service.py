from typing import Optional, List
from sqlmodel import select, Session
from src.testgate.permission.models import Permission
from .schemas import (
    CreatePermissionRequest,
    PermissionQueryParameters,
    UpdatePermissionRequest,
)


def create(
    *, session: Session, permission: CreatePermissionRequest
) -> Optional[Permission]:
    """Creates a new permission object."""

    created_permission = Permission()
    created_permission.name = permission.name

    session.add(created_permission)
    session.commit()
    session.refresh(created_permission)

    return created_permission


def retrieve_by_id(*, session: Session, id: int) -> Optional[Permission]:
    """Return a permission object based on the given id."""

    statement = select(Permission).where(Permission.id == id)

    retrieved_permission = session.exec(statement).one_or_none()

    return retrieved_permission


def retrieve_by_name(*, session: Session, name: str) -> Optional[Permission]:
    """Return a permission object based on the given name."""

    statement = select(Permission).where(Permission.name == name)

    retrieved_permission = session.exec(statement).one_or_none()

    return retrieved_permission


def retrieve_by_query_parameters(
    *, session: Session, query_parameters: PermissionQueryParameters
) -> Optional[List[Permission]]:
    """Return list of permission objects based on the given query parameters."""

    statement = select(Permission)

    for attr, value in query_parameters.dict().items():
        if value:
            statement = statement.filter(getattr(Permission, attr).like(value))

    retrieved_permissions = session.exec(statement).all()

    return retrieved_permissions


def update(
    *,
    session: Session,
    retrieved_permission: Permission,
    permission: UpdatePermissionRequest,
) -> Optional[Permission]:
    """Updates an existing permission object."""

    retrieved_permission.name = permission.name
    updated_permission = retrieved_permission

    session.add(updated_permission)
    session.commit()
    session.refresh(updated_permission)

    return updated_permission


def delete(
    *, session: Session, retrieved_permission: Permission
) -> Optional[Permission]:
    """Deletes an existing permission object."""

    session.delete(retrieved_permission)
    session.commit()

    return retrieved_permission

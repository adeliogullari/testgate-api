from typing import Optional, List, Dict
from jose import jwt
from sqlmodel import select, Session

from ..role.models import Role
from ..team.models import Team

from .models import Plan
from .schemas import *


def retrieve_plan_by_id_service(*, session: Session, id: int) -> Optional[Plan]:
    """Returns a plan based on the given plan id."""

    statement = select(Plan).where(Role.id == id)

    retrieved_plan = session.exec(statement).one_or_none()

    return retrieved_plan


def retrieve_plan_by_name_service(*, session: Session, name: str) -> Optional[Plan]:
    """Returns a plan based on the given plan name."""

    statement = select(Plan).where(Plan.name == name)

    retrieved_plan = session.exec(statement).one_or_none()

    return retrieved_plan


def search_plan_service(*, session: Session, query_parameters: dict) -> Optional[List[Plan]]:
    """Returns a plan object based on the given query parameters."""

    statement = select(Plan)

    for attr, value in query_parameters.items():
        if value:
            statement = statement.filter(getattr(Plan, attr).like(value))

    searched_plan = session.exec(statement).all()

    return searched_plan


def create_plan_service(*, session: Session, plan: CreatePlanRequestModel) -> Optional[Plan]:
    """Creates a new plan."""

    created_plan = Plan(**plan.dict())

    session.add(created_plan)
    session.commit()
    session.refresh(created_plan)

    return created_plan


def update_plan_service(*, session: Session, retrieved_role: Role, plan: UpdatePlanRequestModel) -> Optional[Plan]:
    """Updates an existing plan."""

    for attr, value in plan.dict().items():
        if value:
            setattr(retrieved_role, attr, value)

    updated_plan = Plan(**retrieved_role.dict())

    session.add(updated_plan)
    session.commit()
    session.refresh(updated_plan)

    return updated_plan


def delete_plan_by_id_service(*, session: Session, retrieved_plan: Plan) -> Optional[Plan]:
    """Deletes an existing user."""

    session.delete(retrieved_plan)
    session.commit()

    return retrieved_plan

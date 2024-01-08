from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.execution.models import Execution
from src.testgate.database.models import UserRepositoryLink

if TYPE_CHECKING:
    from src.testgate.user.models import User


class Repository(SQLModel, table=True):
    __tablename__ = "repository"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    users: list["User"] = Relationship(
        back_populates="repositories", link_model=UserRepositoryLink
    )
    executions: list[Execution] = Relationship(back_populates="repository")


Execution.model_rebuild()

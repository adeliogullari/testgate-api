from bcrypt import hashpw, gensalt, checkpw
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from ..role.models import Role
from ..team.models import Team


class User(SQLModel, table=True):

    __tablename__ = "user"

    id: Optional[int] = Field(primary_key=True)
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    email: str = Field(default=None, unique=True)
    password: str = Field(default=None)
    verified: bool = Field(default=False)
    image: str = Field(default=None, unique=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users")
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="users")

    def generate_password(self):
        return hashpw(bytes(self.password, 'UTF-8'), gensalt())

    def check_password(self, password: str):
        return checkpw(password.encode("UTF-8"), bytes(self.password, encoding="UTF-8"))


Role.update_forward_refs()
Team.update_forward_refs()

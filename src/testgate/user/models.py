from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from ..role.models import Role
from ..team.models import Team
from ..repository.models import Repository
from ..link.models import UserRepositoryLink
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_pash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class User(SQLModel, table=True):

    __tablename__ = "user"

    id: Optional[int] = Field(primary_key=True)
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    username: str = Field(default=None)
    email: str = Field(default=None, unique=True)
    password: str = Field(default=None)
    verified: bool = Field(default=False)
    image: str = Field(default=None)
    repositories: List["Repository"] = Relationship(back_populates="users", link_model=UserRepositoryLink)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users")
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="users")

    def generate_password(self):
        return password_pash_library.encode(self.password)
        # return hashpw(bytes(self.password, 'UTF-8'), gensalt())

    def check_password(self, password: str):
        return password_pash_library.verify(password, self.password)
        # return checkpw(password.encode("UTF-8"), bytes(self.password, encoding="UTF-8"))


Role.update_forward_refs()
Team.update_forward_refs()

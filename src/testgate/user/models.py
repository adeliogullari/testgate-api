from pydantic import EmailStr
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from src.testgate.role.models import Role
from src.testgate.repository.models import Repository
from src.testgate.link.models import UserRepositoryLink
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy

password_pash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    password: Optional[str] = Field(default=None)
    verified: bool = Field(default=False)
    image: Optional[str] = Field(default=None)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="users")
    repositories: List[Repository] = Relationship(
        back_populates="users", link_model=UserRepositoryLink
    )

    def generate_password(self):
        return password_pash_library.encode(password=self.password)

    def check_password(self, password: str):
        return password_pash_library.verify(
            password=password, encoded_password=self.password
        )


Role.update_forward_refs()
Repository.update_forward_refs()

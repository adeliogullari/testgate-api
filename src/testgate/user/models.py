from sqlmodel import SQLModel, Field, Relationship
from src.testgate.role.models import Role
from src.testgate.repository.models import Repository
from src.testgate.database.models import UserRepositoryLink
from src.testgate.auth.crypto.password.library import PasswordHashLibrary

password_pash_library = PasswordHashLibrary(algorithm="scrypt")


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: bytes = Field(default=None)
    verified: bool = Field(default=False)
    image: str | None = Field(default=None)
    role_id: int | None = Field(default=None, foreign_key="role.id")
    role: Role = Relationship(back_populates="users")
    repositories: list[Repository] = Relationship(
        back_populates="users", link_model=UserRepositoryLink
    )

    def check_password(self, password: str) -> bool:
        return password_pash_library.verify(
            password=password, encoded_password=self.password
        )


Role.model_rebuild()
Repository.model_rebuild()

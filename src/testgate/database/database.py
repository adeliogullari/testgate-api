from typing import Any, Generator
from alembic import command
from alembic.config import Config
from sqlmodel import Session, SQLModel, create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://admin:secret@localhost:5432/testgate_postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

alembic_cfg = Config()
alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
alembic_cfg.set_main_option("script_location", "src/alembic/")


def run_db_migrations() -> None:
    command.upgrade(alembic_cfg, "head")


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, Any]:
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session

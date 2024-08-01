from typing import Any, AsyncGenerator
from config import Settings
from alembic import command
from alembic.config import Config
from sqlmodel import Session, SQLModel, create_engine

settings = Settings()

schema = settings.testgate_postgresql_schema
host = settings.testgate_postgresql_host
port = settings.testgate_postgresql_port
user = settings.testgate_postgresql_user
password = settings.testgate_postgresql_password
database = settings.testgate_postgresql_database
url = f"{schema}://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(url=url, echo=True)

alembic_cfg = Config()
alembic_cfg.set_main_option("sqlalchemy.url", url)
alembic_cfg.set_main_option("script_location", "alembic")


async def get_sqlmodel_session() -> AsyncGenerator[Session, Any]:
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session


def run_db_migrations() -> None:
    command.upgrade(alembic_cfg, "head")


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

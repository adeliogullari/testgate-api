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

SQLALCHEMY_DATABASE_URL = f"{schema}://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

alembic_cfg = Config()
alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
alembic_cfg.set_main_option("script_location", "src/alembic/")


def run_db_migrations():
    command.upgrade(alembic_cfg, "head")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session

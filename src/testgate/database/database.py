from alembic import command
from alembic.config import Config
from sqlmodel import Session, SQLModel, create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://admin:secret@localhost:5432/testgate_postgres"

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

# from sqlalchemy.orm import Session
#
# from app import crud, schemas
# from app.core.config import settings
# from app.db import base  # noqa: F401
#
# # make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# # otherwise, SQL Alchemy might fail to initialize relationships properly
# # for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
#
#
# def init_db(db: Session) -> None:
#     # Tables should be created with Alembic migrations
#     # But if you don't want to use migrations, create
#     # the tables un-commenting the next line
#     # Base.metadata.create_all(bind=engine)
#
#     user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
#     if not user:
#         user_in = schemas.UserCreate(
#             email=settings.FIRST_SUPERUSER,
#             password=settings.FIRST_SUPERUSER_PASSWORD,
#             is_superuser=True,
#         )
#         user = crud.user.create(db, obj_in=user_in)  # noqa: F841

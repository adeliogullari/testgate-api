from sqlmodel import Session, SQLModel, create_engine
from src.testgate.role.models import Role
from alembic import command
from alembic.config import Config
from src.testgate.role.schemas import CreateRoleRequestModel
from src.testgate.role.service import upsert_role_service
from src.testgate.auth.schemas import CreateUserRequestModel
from src.testgate.auth.service import upsert_user_service

SQLALCHEMY_DATABASE_URL = "postgresql://admin:secret@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # with Session(engine) as session:
        # upsert_role_service(session=session, role=CreateRoleRequestModel(**{'name': "Admin"}))
        # upsert_user_service(session=session, user=CreateUserRequestModel(**{"firstname": "admin",
        #                                                                     "lastname": "admin",
        #                                                                     "email": "admin@admin.com",
        #                                                                     "password": "secret",
        #                                                                     "verified": True,
        #                                                                     "roles": ["Admin"],
        #                                                                     "teams": []}))

    # alembic_cfg = Config()
    # alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    # alembic_cfg.set_main_option("script_location", "src/alembic/")
    # command.upgrade(alembic_cfg, "head")

    # with Session(engine) as session:
    #     session.add(Role(name="Admin", users=[]))
    #     session.commit()

def get_session():
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session

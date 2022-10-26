import pytest
from pytest_factoryboy import register
from src.testgate.project.models import Project
from factory.alchemy import SQLAlchemyModelFactory


class ProjectFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Project
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = "MyProject"
    teams = []
    runs = []


@pytest.fixture(autouse=True)
def set_session_for_project_factory(db_session):
    ProjectFactory._meta.sqlalchemy_session = db_session


register(ProjectFactory)

import pytest
from src.testgate.team.models import Team
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker
import factory


class TeamFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Team
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = Faker('name')
    users = [] #factory.RelatedFactoryList('tests.user.conftest.UserFactory', 'team', size=3)


@pytest.fixture(autouse=True)
def set_session_for_team_factory(db_session):
    TeamFactory._meta.sqlalchemy_session = db_session


register(TeamFactory)

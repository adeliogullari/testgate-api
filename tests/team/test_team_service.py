from src.testgate.team.service import create, retrieve_by_id, retrieve_by_name, retrieve_by_query_parameters, update, delete


def test_create(db_session, team_factory):

    team = team_factory.stub()

    created_team = create(session=db_session, team=team)

    assert created_team.name == team.name


def test_retrieve_by_id(db_session, team):

    retrieved_team = retrieve_by_id(session=db_session, id=team.id)

    assert retrieved_team.id == team.id


def test_retrieve_by_name(db_session, team):

    retrieved_team = retrieve_by_name(session=db_session, name=team.name)

    assert retrieved_team.name == team.name


def test_retrieve_by_query_parameters(db_session, team):

    retrieved_team = retrieve_by_query_parameters(session=db_session, query_parameters={'name': team.name})

    assert retrieved_team[0].name == team.name


def test_update(db_session, team_factory, team):

    updated_team = update(session=db_session, retrieved_team=team, team=team_factory.stub())

    assert updated_team.id == team.id


def test_delete(db_session, team):

    deleted_team = delete(session=db_session, retrieved_team=team)

    assert deleted_team.id == team.id

from src.testgate.suite.service import create, retrieve_by_id, retrieve_by_name, update, delete


def test_create(db_session, suite_factory):

    suite = suite_factory.stub()

    created_suite = create(session=db_session, suite=suite)

    assert created_suite.name == created_suite.name


def test_retrieve_by_id(db_session, suite):

    retrieved_suite = retrieve_by_id(session=db_session, id=suite.id)

    assert retrieved_suite.id == suite.id


def test_retrieve_by_name(db_session, suite):

    retrieved_suite = retrieve_by_name(session=db_session, name=suite.name)

    assert retrieved_suite.id == suite.id

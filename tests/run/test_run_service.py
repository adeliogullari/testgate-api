from src.testgate.run.service import create, retrieve_by_id, retrieve_by_name, retrieve_by_query_parameters, update, delete


def test_create(db_session, run_factory):

    run = run_factory.stub()

    created_run = create(session=db_session, run=run)

    assert created_run.name == created_run.name


def test_retrieve_by_id(db_session, run):

    retrieved_run = retrieve_by_id(session=db_session, id=run.id)

    assert retrieved_run.id == run.id


def test_retrieve_by_name(db_session, run):

    retrieved_run = retrieve_by_name(session=db_session, name=run.name)

    assert retrieved_run.name == run.name


def test_retrieve_by_query_parameters(db_session, run):

    retrieved_run = retrieve_by_query_parameters(session=db_session, query_parameters={'name': run.name})

    assert retrieved_run[0].name == run.name


def test_update(db_session, run_factory, run):

    updated_run = update(session=db_session, retrieved_run=run, run=run_factory.stub())

    assert updated_run.id == run.id


def test_delete(db_session, run):

    deleted_run = delete(session=db_session, retrieved_run=run)

    assert deleted_run.id == run.id

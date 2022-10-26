from src.testgate.project.service import create, retrieve_by_id, retrieve_by_name, retrieve_by_query_parameters, update, delete


def test_create(db_session, project_factory):

    project = project_factory.stub()

    created_project = create(session=db_session, project=project)

    assert created_project.name == project.name


def test_retrieve_by_id(db_session, project):

    retrieved_project = retrieve_by_id(session=db_session, id=project.id)

    assert retrieved_project.id == project.id


def test_retrieve_by_name(db_session, project):

    retrieved_project = retrieve_by_name(session=db_session, name=project.name)

    assert retrieved_project.name == project.name


def test_retrieve_by_query_parameters(db_session, project):

    retrieved_project = retrieve_by_query_parameters(session=db_session, query_parameters={'name': project.name})

    assert retrieved_project[0].name == project.name


def test_update(db_session, project_factory, project):

    updated_project = update(session=db_session, retrieved_project=project, project=project_factory.stub())

    assert updated_project.id == project.id


def test_delete(db_session, project):

    deleted_project = delete(session=db_session, retrieved_project=project)

    assert deleted_project.id == project.id

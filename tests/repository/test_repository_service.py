from src.testgate.repository.service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)

from src.testgate.repository.schemas import (
    CreateRepositoryRequest,
    RepositoryQueryParameters,
    UpdateRepositoryRequest,
)


def test_create(db_session, repository_factory):
    repository = CreateRepositoryRequest(**repository_factory.stub().__dict__)

    created_repository = create(session=db_session, repository=repository)

    assert created_repository.name == repository.name


def test_retrieve_by_id(db_session, repository):
    retrieved_repository = retrieve_by_id(session=db_session, id=repository.id)

    assert retrieved_repository.id == repository.id


def test_retrieve_by_name(db_session, repository):
    retrieved_repository = retrieve_by_name(session=db_session, name=repository.name)

    assert retrieved_repository.name == repository.name


def test_retrieve_by_query_parameters(db_session, repository):
    query_parameters = RepositoryQueryParameters(**repository.__dict__)

    retrieved_repository = retrieve_by_query_parameters(
        session=db_session, query_parameters=query_parameters
    )

    assert retrieved_repository[0].id == repository.id


def test_update(db_session, repository_factory, repository):
    update_repository = UpdateRepositoryRequest(**repository_factory.stub().__dict__)

    updated_repository = update(
        session=db_session,
        retrieved_repository=repository,
        repository=update_repository,
    )

    assert updated_repository.id == repository.id


def test_delete(db_session, repository):
    deleted_repository = delete(session=db_session, retrieved_repository=repository)

    assert deleted_repository.id == repository.id

from src.testgate.execution.service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    retrieve_by_query_parameters,
    update,
    delete,
)

from src.testgate.execution.schemas import (
    CreateExecutionRequest,
    ExecutionQueryParameters,
    UpdateExecutionRequest,
)


def test_create(db_session, execution_factory):
    execution = CreateExecutionRequest(**execution_factory.stub().__dict__)

    created_execution = create(session=db_session, execution=execution)

    assert created_execution.name == execution.name


def test_retrieve_by_id(db_session, execution):
    retrieved_execution = retrieve_by_id(session=db_session, id=execution.id)

    assert retrieved_execution.id == execution.id


def test_retrieve_by_name(db_session, execution):
    retrieved_execution = retrieve_by_name(session=db_session, name=execution.name)

    assert retrieved_execution.name == execution.name


def test_retrieve_by_query_parameters(db_session, execution):
    query_parameters = ExecutionQueryParameters(**execution.__dict__)

    retrieved_execution = retrieve_by_query_parameters(
        session=db_session, query_parameters=query_parameters
    )

    assert retrieved_execution[0].id == execution.id


def test_update(db_session, execution_factory, execution):
    update_execution = UpdateExecutionRequest(**execution_factory.stub().__dict__)

    update_execution = update(
        session=db_session, retrieved_execution=execution, execution=update_execution
    )

    assert update_execution.id == execution.id


def test_delete(db_session, execution):
    deleted_execution = delete(session=db_session, retrieved_execution=execution)

    assert deleted_execution.id == execution.id

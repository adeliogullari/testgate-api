from src.testgate.case.models import Case
from src.testgate.case.schemas import (
    CaseQueryParameters,
    CreateCaseRequestModel,
    UpdateCaseRequestModel,
)
from src.testgate.case.service import (
    create,
    retrieve_by_id,
    retrieve_by_query_parameters,
    update,
    delete,
)


def test_create(db_session, case_factory):
    case = CreateCaseRequestModel(**case_factory.stub().__dict__)

    created_case = create(session=db_session, case=case)

    assert created_case.name == case.name


def test_retrieve_by_id(db_session, case):
    retrieved_case = retrieve_by_id(session=db_session, case_id=case.id)

    assert retrieved_case.id == case.id


def test_retrieve_by_query_parameters(db_session, case: Case):
    query_parameters = CaseQueryParameters(offset=0, limit=1, name=case.name)

    retrieved_cases = retrieve_by_query_parameters(
        session=db_session, query_parameters=query_parameters
    )

    assert retrieved_cases[0].id == case.id


def test_update(db_session, case_factory, case: Case):
    update_case = UpdateCaseRequestModel(**case_factory.stub().__dict__)

    updated_case = update(session=db_session, retrieved_case=case, case=update_case)

    assert updated_case.id == case.id


def test_delete(db_session, case: Case):
    deleted_case = delete(session=db_session, retrieved_case=case)

    assert deleted_case.id == case.id

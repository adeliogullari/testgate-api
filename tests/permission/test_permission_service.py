from src.testgate.permission.service import (create,
                                             retrieve_by_id,
                                             retrieve_by_name,
                                             retrieve_by_query_parameters,
                                             update,
                                             delete)

from src.testgate.permission.schemas import CreatePermissionRequest, PermissionQueryParameters, UpdatePermissionRequest


def test_create(db_session, permission_factory):
    permission = CreatePermissionRequest(**permission_factory.stub().__dict__)

    created_permission = create(session=db_session, permission=permission)

    assert created_permission.name == permission.name


def test_retrieve_by_id(db_session, permission):
    retrieved_permission = retrieve_by_id(session=db_session, id=permission.id)

    assert retrieved_permission.id == permission.id


def test_retrieve_by_name(db_session, permission):
    retrieved_permission = retrieve_by_name(session=db_session, name=permission.name)

    assert retrieved_permission.name == permission.name


def test_retrieve_by_query_parameters(db_session, permission):
    query_parameters = PermissionQueryParameters(**permission.__dict__)

    retrieved_permission = retrieve_by_query_parameters(session=db_session, query_parameters=query_parameters)

    assert retrieved_permission[0].id == permission.id


def test_update(db_session, permission_factory, permission):
    update_permission = UpdatePermissionRequest(**permission_factory.stub().__dict__)

    updated_permission = update(session=db_session, retrieved_permission=permission, permission=update_permission)

    assert updated_permission.id == permission.id


def test_delete(db_session, permission):
    deleted_permission = delete(session=db_session, retrieved_permission=permission)

    assert deleted_permission.id == permission.id

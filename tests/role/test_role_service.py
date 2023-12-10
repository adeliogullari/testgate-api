from src.testgate.role.service import (
    create,
    retrieve_by_id,
    retrieve_by_name,
    update,
    delete,
)
from src.testgate.role.schemas import CreateRoleRequestModel, UpdateRoleRequestModel


def test_create(db_session, role_factory):
    role = CreateRoleRequestModel(**role_factory.stub().__dict__)

    created_role = create(session=db_session, role=role)

    assert created_role.name == role.name


def test_retrieve_by_id(db_session, role):
    retrieved_role = retrieve_by_id(session=db_session, id=role.id)

    assert retrieved_role.id == role.id


def test_retrieve_by_name(db_session, role):
    retrieved_role = retrieve_by_name(session=db_session, name=role.name)

    assert retrieved_role.name == role.name


def test_update(db_session, role_factory, role):
    updated_role = update(
        session=db_session,
        retrieved_role=role,
        role=UpdateRoleRequestModel(**role_factory.stub().__dict__),
    )

    assert updated_role.id == role.id


def test_delete(db_session, role):
    deleted_role = delete(session=db_session, retrieved_role=role)

    assert deleted_role.id == role.id

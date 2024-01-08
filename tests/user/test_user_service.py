import pytest
from src.testgate.user.models import User
from src.testgate.user.schemas import (
    UserQueryParametersModel,
    CreateUserRequestModel,
    UpdateUserRequestModel,
)
from src.testgate.user.service import (
    retrieve_by_id,
    retrieve_by_username,
    retrieve_by_email,
    retrieve_by_query_parameters,
    create,
    update,
    update_password,
    verify,
    delete,
)


def test_retrieve_by_id(db_session, user: User):
    retrieved_user = retrieve_by_id(session=db_session, user_id=user.id)

    assert retrieved_user.id == user.id


def test_retrieve_by_username(db_session, user: User):
    retrieved_user = retrieve_by_username(
        session=db_session, user_username=user.username
    )

    assert retrieved_user.username == user.username


def test_retrieve_by_email(db_session, user: User):
    retrieved_user = retrieve_by_email(session=db_session, user_email=user.email)

    assert retrieved_user.email == user.email


def test_retrieve_by_query_parameters(db_session, user: User):
    query_parameters = UserQueryParametersModel(
        offset=0,
        limit=1,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        verified=user.verified,
    )

    retrieved_users = retrieve_by_query_parameters(
        session=db_session, query_parameters=query_parameters
    )

    assert retrieved_users[0].id == user.id


def test_create(db_session, user_factory):
    user = CreateUserRequestModel(**user_factory.stub().__dict__)

    created_user = create(session=db_session, user=user)

    assert created_user.email == user.email


def test_update(db_session, user_factory, user: User):
    update_user = UpdateUserRequestModel(**user_factory.stub().__dict__)

    updated_user = update(session=db_session, retrieved_user=user, user=update_user)

    assert updated_user.id == user.id


def test_update_password(db_session, user_factory, user: User):
    retrieved_user = user_factory.stub()

    updated_user = update_password(
        session=db_session, retrieved_user=user, password=retrieved_user.password
    )

    assert updated_user.password == user.password


def test_verify(db_session, user):
    verified_user = verify(session=db_session, retrieved_user=user)

    assert verified_user.verified is True


def test_delete(db_session, user: User):
    deleted_user = delete(session=db_session, retrieved_user=user)

    assert deleted_user.id == user.id

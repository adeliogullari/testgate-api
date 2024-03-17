from sqlmodel import Session
from src.testgate.auth.crypto.password.library import PasswordHashLibrary
from src.testgate.auth.crypto.password.strategy import ScryptPasswordHashStrategy
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

password_pash_library = PasswordHashLibrary(ScryptPasswordHashStrategy())


async def test_retrieve_by_id(sqlmodel_session: Session, user: User):
    retrieved_user = await retrieve_by_id(
        sqlmodel_session=sqlmodel_session, user_id=user.id
    )

    assert retrieved_user.id == user.id


async def test_retrieve_by_username(sqlmodel_session: Session, user: User):
    retrieved_user = await retrieve_by_username(
        sqlmodel_session=sqlmodel_session, user_username=user.username
    )

    assert retrieved_user.username == user.username


async def test_retrieve_by_email(sqlmodel_session: Session, user: User):
    retrieved_user = await retrieve_by_email(
        sqlmodel_session=sqlmodel_session, user_email=user.email
    )

    assert retrieved_user.email == user.email


async def test_retrieve_by_query_parameters(sqlmodel_session: Session, user: User):
    query_parameters = UserQueryParametersModel(
        offset=0,
        limit=1,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        verified=user.verified,
    )

    retrieved_users = await retrieve_by_query_parameters(
        sqlmodel_session=sqlmodel_session, query_parameters=query_parameters
    )

    assert retrieved_users[0].id == user.id


async def test_create(sqlmodel_session: Session, user_factory):
    user = CreateUserRequestModel(
        **user_factory.stub(password="password_2024").__dict__
    )

    created_user = await create(sqlmodel_session=sqlmodel_session, user=user)

    assert created_user.email == user.email


async def test_update(sqlmodel_session: Session, user_factory, user: User):
    update_user = UpdateUserRequestModel(
        **user_factory.stub(password="password_2024").__dict__
    )

    updated_user = await update(
        sqlmodel_session=sqlmodel_session, retrieved_user=user, user=update_user
    )

    assert updated_user.id == user.id


async def test_update_password(sqlmodel_session: Session, user_factory, user: User):
    retrieved_user = user_factory.stub(
        password=password_pash_library.encode("password_2024")
    )

    updated_user = await update_password(
        sqlmodel_session=sqlmodel_session,
        retrieved_user=user,
        password=retrieved_user.password,
    )

    assert updated_user.password == user.password


async def test_verify(sqlmodel_session: Session, user):
    verified_user = await verify(sqlmodel_session=sqlmodel_session, retrieved_user=user)

    assert verified_user.verified is True


async def test_delete(sqlmodel_session: Session, user: User):
    deleted_user = await delete(sqlmodel_session=sqlmodel_session, retrieved_user=user)

    assert deleted_user.id == user.id

from jose import jwt

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .service import *
from .exceptions import *
from ..role.service import retrieve_role_by_name_service
from ..team.service import retrieve_team_by_name_service
from .schemas import RetrieveUserResponseModel, \
    RetrieveCurrentUserResponseModel, \
    SearchUserQueryParametersModel, \
    SearchUserResponseModel, \
    CreateUserResponseModel, \
    UpdateUserResponseModel, \
    DeleteUserResponseModel, \
    AuthenticateUserRequestModel, \
    AuthenticateUserResponseModel
from .constants import *

from ..database.database import get_session
from ..email import EmailService

auth_router = APIRouter()
user_router = APIRouter(tags=["users"])


@user_router.get(path="/api/v1/users/me",
                 response_model=RetrieveCurrentUserResponseModel,
                 status_code=200)
def retrieve_current_user_by_access_token(*,
                                          session: Session = Depends(get_session),
                                          http_authorization_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Retrieves current user by access token."""

    token = http_authorization_credentials.credentials
    payload = jwt.decode(token=token, key=JWT_ACCESS_TOKEN_KEY, algorithms=JWT_ACCESS_TOKEN_ALG)
    email = payload.get("email")

    retrieved_user = retrieve_user_by_email_service(session=session, email=email)

    return retrieved_user


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(retrieve_current_user_by_access_token)):
        if current_user.roles != self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


allow_create_resource = RoleChecker(["admin"])


@user_router.get(path="/api/v1/user/{id}",
                 response_model=RetrieveUserResponseModel,
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def retrieve_user_by_id(*, session: Session = Depends(get_session), id: int):
    """Retrieves user by id."""

    retrieved_user = retrieve_user_by_id_service(session=session, id=id)

    if not retrieved_user:
        raise UserNotFoundException

    return retrieved_user


@user_router.get(path="/api/v1/users",
                 response_model=List[SearchUserResponseModel],
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def search_user(*,
                session: Session = Depends(get_session),
                offset: int = 0,
                limit: int = Query(default=100, lte=100),
                firstname: str = None,
                lastname: str = None,
                email: str = None,
                roles: List[str] = Query([]),
                teams: List[str] = Query([])):
    """Search user by firstname, lastname, email, roles and teams"""

    roles = [retrieve_role_by_name_service(session=session, name=role) for role in roles]
    teams = [retrieve_role_by_name_service(session=session, name=team) for team in teams]

    query_parameters = SearchUserQueryParametersModel(offset=offset,
                                                      limit=limit,
                                                      firstname=firstname,
                                                      lastname=lastname,
                                                      email=email,
                                                      roles=roles,
                                                      teams=teams)

    searched_user = search_user_service(session=session, query_parameters=query_parameters)

    return searched_user


@user_router.post(path="/api/v1/user",
                  response_model=CreateUserResponseModel,
                  status_code=201)
def create_user(*, session: Session = Depends(get_session), user: CreateUserRequestModel):
    """Create user."""

    retrieved_user = retrieve_user_by_email_service(session=session, email=user.email)

    if retrieved_user:
        raise UserAlreadyExistsException

    user.roles = [retrieve_role_by_name_service(session=session, name=name) for name in user.roles]
    user.teams = [retrieve_team_by_name_service(session=session, name=name) for name in user.teams]

    created_user = create_user_service(session=session, user=user)

    # email_service = EmailService()
    # email_service.email_subject = "Email Verification"
    # email_service.email_from = SMTP_EMAIL_ADDRESS
    # email_service.email_to = user.email
    # email_service.email_password = SMTP_EMAIL_APP_PASSWORD
    #
    # email_service.add_plain_text_message("Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org")
    # email_service.add_html_message(
    #     """\
    #         <html>
    #             <head></head>
    #             <body>
    #                 <p>
    #                     Hi!
    #                     <br>How are you?<br>
    #                     Here is the <a href="http://www.python.org">link</a> you wanted.
    #                 </p>
    #             </body>
    #         </html>
    #     """)
    # email_service.send_email()
    return created_user


@user_router.put(path="/api/v1/user/{id}",
                 response_model=UpdateUserResponseModel,
                 status_code=200,
                 dependencies=[Depends(allow_create_resource)])
def update_user(*, session: Session = Depends(get_session), id: int, user: UpdateUserRequestModel):

    retrieved_user = retrieve_user_by_id_service(session=session, id=id)

    if not retrieved_user:
        raise UserNotFoundException

    roles = [retrieve_role_by_name_service(session=session, name=role) for role in user.roles]
    teams = [retrieve_role_by_name_service(session=session, name=team) for team in user.teams]

    user.roles = roles
    user.teams = teams

    updated_user = update_user_service(session=session, retrieved_user=retrieved_user, user=user)

    return updated_user


@user_router.put(path="/api/v1/users/me",
                 response_model=UpdateUserResponseModel,
                 status_code=200)
def update_current_user_by_access_token(*,
                                        session: Session = Depends(get_session),
                                        user: UpdateUserRequestModel,
                                        http_authorization_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Update current user by access token."""

    token = http_authorization_credentials.credentials
    payload = jwt.decode(token=token, key=JWT_ACCESS_TOKEN_KEY, algorithms=JWT_ACCESS_TOKEN_ALG)
    email = payload.get("email")

    retrieved_user = retrieve_user_by_email_service(session=session, email=email)

    user.roles = [retrieve_role_by_name_service(session=session, name=role) for role in user.roles]
    user.teams = [retrieve_team_by_name_service(session=session, name=team) for team in user.teams]

    updated_user = update_user_service(session=session, retrieved_user=retrieved_user, user=user)

    return updated_user


@user_router.get(path="/api/v1/user/email/verify/{token}",
                 response_model=UpdateUserResponseModel,
                 status_code=200)
def verify_current_user(*, session: Session = Depends(get_session), token: str):
    payload = jwt.decode(token=token, key=JWT_ACCESS_TOKEN_KEY, algorithms=JWT_ACCESS_TOKEN_ALG)
    email = payload.get("email")

    retrieved_user = retrieve_user_by_email_service(session=session, email=email)

    if not retrieved_user:
        raise UserNotFoundException

    user = UpdateUserRequestModel()
    user.verified = True

    updated_user = update_user_service(session=session, retrieved_user=retrieved_user, user=user)

    return updated_user


@user_router.post("/api/v1/user/auth", response_model=AuthenticateUserResponseModel, status_code=200)
def authenticate_user(*, session: Session = Depends(get_session), authentication: AuthenticateUserRequestModel):
    retrieved_user = retrieve_user_by_email_service(session=session, email=authentication.email)

    if not retrieved_user:
        raise UserEmailNotFoundException

    if not retrieved_user.check_password(authentication.password):
        raise InvalidPasswordException

    return retrieved_user


@user_router.delete(path="/api/v1/user/me",
                    response_model=DeleteUserResponseModel,
                    status_code=200)
def delete_current_user_by_access_token(*,
                                        session: Session = Depends(get_session),
                                        http_authorization_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = http_authorization_credentials.credentials
    payload = jwt.decode(token=token, key=JWT_ACCESS_TOKEN_KEY, algorithms=JWT_ACCESS_TOKEN_ALG)
    email = payload.get("email")
    retrieved_user = retrieve_user_by_email_service(session=session, email=email)

    if not retrieved_user:
        raise UserNotFoundException

    deleted_user = delete_user_service(session=session, retrieved_user=retrieved_user)

    return deleted_user


@user_router.delete(path="/api/v1/user/{id}",
                    response_model=DeleteUserResponseModel,
                    status_code=200,
                    dependencies=[Depends(allow_create_resource)])
def delete_user(*, session: Session = Depends(get_session), id: int):
    retrieved_user = retrieve_user_by_id_service(session=session, id=id)

    if not retrieved_user:
        raise UserNotFoundException

    deleted_user = delete_user_service(session=session, retrieved_user=retrieved_user)

    return deleted_user

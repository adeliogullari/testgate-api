from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

InvalidAccessTokenException = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Access token is invalid"
)

InvalidRefreshTokenException = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Refresh token is invalid"
)

UserNotFoundByIdException = HTTPException(
    status_code=HTTP_404_NOT_FOUND, detail="A user with this id does not exist"
)

UserNotFoundByEmailException = HTTPException(
    status_code=HTTP_404_NOT_FOUND, detail="A user with this email does not exist"
)

UserIdAlreadyExistsException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A user with this id already exists"
)

UserUsernameAlreadyExistsException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A user with this username already exists"
)

UserEmailAlreadyExistsException = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="A user with this email already exists"
)

InvalidPasswordException = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Password is invalid"
)

InvalidPasswordConfirmationException = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Password confirmation is invalid"
)

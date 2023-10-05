from fastapi import HTTPException
from starlette.status import (HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND,
                              HTTP_409_CONFLICT)


UserNotFoundException = HTTPException(status_code=HTTP_404_NOT_FOUND,
                                      detail="A user with this id does not exist")

UserAlreadyExistsException = HTTPException(status_code=HTTP_409_CONFLICT,
                                           detail="A user with this id already exists")

UserEmailNotFoundException = HTTPException(status_code=HTTP_404_NOT_FOUND,
                                           detail="User email does not exist")

UserEmailAlreadyExistsException = HTTPException(status_code=HTTP_409_CONFLICT,
                                                detail="User email already exists")

InvalidPasswordException = HTTPException(status_code=HTTP_403_FORBIDDEN,
                                         detail="User password is invalid")

InvalidPasswordConfirmationException = HTTPException(status_code=HTTP_403_FORBIDDEN,
                                                     detail="Password confirmation is invalid")

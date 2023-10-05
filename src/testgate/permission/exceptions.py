from fastapi import status, HTTPException

PermissionNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail="A permission with that id does not exist")

PermissionAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                                 detail="A permission with that id already exists")

from fastapi import status, HTTPException

RepositoryNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="A repository with that id does not exist",
)

RepositoryAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A repository with that id already exists",
)

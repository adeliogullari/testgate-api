from fastapi import status, HTTPException

ExecutionNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="A execution with that id does not exist",
)

ExecutionAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A execution with that id already exists",
)

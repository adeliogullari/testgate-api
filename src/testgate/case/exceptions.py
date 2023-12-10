from fastapi import status, HTTPException


CaseNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="A case with that id does not exist"
)

CaseAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="A case with that id already exists"
)

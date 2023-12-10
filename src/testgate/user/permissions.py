from sqlmodel import Session
from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.testgate.user.models import User
from src.testgate.user.views import retrieve_current_user


class RoleChecker:
    def __init__(self, roles: list[str], permission: Optional[str]):
        self.roles = roles
        self.permission = permission

    def __call__(self, current_user: User = Depends(retrieve_current_user)):
        if current_user.role.name not in self.roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


user_permission = RoleChecker(["Admin"], None)

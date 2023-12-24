from typing import Optional
from fastapi import Depends, HTTPException

from src.testgate.user.models import User
from src.testgate.user.views import retrieve_current_user


class RoleChecker:
    def __init__(self, roles: list[str], permission: Optional[str]):
        self.roles = roles
        self.permission = permission

    def __call__(self, current_user: User = Depends(retrieve_current_user)):
        if current_user.role.name not in self.roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


class RolePermission:
    def __init__(self, roles: list[str], permission: Optional[str]):
        self.roles = roles
        self.permission = permission

    def __call__(self, current_user: User = Depends(retrieve_current_user)):
        if current_user.role.name not in self.roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


isAdmin = RolePermission(["Admin"], None)

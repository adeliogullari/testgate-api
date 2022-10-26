# from typing import List, TYPE_CHECKING
# from .views import retrieve_current_user_by_access_token
# from fastapi import Depends, HTTPException
# from models import User
#
#
# class Permission:
#
#     def __init__(self):
#         pass
#
#     def compare_roles(self, roles, permitted_roles):
#         return list(set(roles).intersection(set(permitted_roles))) is not []
#
#
# class UserPermission(Permission):
#
#     def __init__(self, roles: List):
#         super().__init__()
#         self.roles = roles
#
#     def __call__(self, current_user: User = Depends(retrieve_current_user_by_access_token)):
#         if self.compare_roles(current_user.roles, self.roles):
#             raise HTTPException(status_code=403, detail="Operation not permitted")
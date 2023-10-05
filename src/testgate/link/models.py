from typing import Optional
from sqlmodel import SQLModel, Field


class UserRepositoryLink(SQLModel, table=True):

    __tablename__ = "user_repository"

    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    repository_id: Optional[int] = Field(default=None, foreign_key="repository.id", primary_key=True)


class TeamProjectLink(SQLModel, table=True):

    __tablename__ = "team_project"

    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)


class ProjectRunLink(SQLModel, table=True):

    __tablename__ = "project_run"

    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
    run_id: Optional[int] = Field(default=None, foreign_key="run.id", primary_key=True)


class RolePermissionLink(SQLModel, table=True):

    __tablename__ = "role_permission"

    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: Optional[int] = Field(default=None, foreign_key="permission.id", primary_key=True)


# class RolePermissionLink(SQLModel, table=True):
#
#     __tablename__ = "role_permission"
#
#     role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)
#     permission_id: Optional[int] = Field(default=None, foreign_key="permission.id", primary_key=True)



# class ProjectPlanLink(SQLModel, table=True):
#
#     __tablename__ = "project_plan"
#
#     project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
#     plan_id: Optional[int] = Field(default=None, foreign_key="plan.id", primary_key=True)


# class PlanSuiteLink(SQLModel, table=True):
#
#     __tablename__ = "plan_suite"
#
#     plan_id: Optional[int] = Field(default=None, foreign_key="plan.id", primary_key=True)
#     suite_id: Optional[int] = Field(default=None, foreign_key="suite.id", primary_key=True)
#
#
# class SuiteCaseLink(SQLModel, table=True):
#
#     __tablename__ = "suite_case"
#
#     suite_id: Optional[int] = Field(default=None, foreign_key="suite.id", primary_key=True)
#     case_id: Optional[int] = Field(default=None, foreign_key="case.id", primary_key=True)

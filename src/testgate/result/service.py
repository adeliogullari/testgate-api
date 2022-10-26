# from typing import Optional, List
# from sqlmodel import select, Session
# from .models import Result
# from .schemas import CreateResultRequestModel, UpdateResultRequestModel
#
#
# def create(*, session: Session, result: CreateResultRequestModel) -> Optional[Result]:
#     """Creates a new result object."""
#
#     created_result = Result()
#     created_result.name = result.name
#     created_result.total = result.total
#     created_result.passed = result.passed
#     created_result.failed = result.failed
#     created_result.skipped = result.skipped
#
#     session.add(created_result)
#     session.commit()
#     session.refresh(created_result)
#
#     return created_result
#
#
# def retrieve_by_id(*, session: Session, id: int) -> Optional[Result]:
#     """Return a result object based on the given id."""
#
#     statement = select(Result).where(Result.id == id)
#
#     retrieved_result = session.exec(statement).one_or_none()
#
#     return retrieved_result
#
#
# def retrieve_by_name(*, session: Session, name: str) -> Optional[Result]:
#     """Return a result object based on the given name."""
#
#     statement = select(Result).where(Result.name == name)
#
#     retrieved_result = session.exec(statement).one_or_none()
#
#     return retrieved_result
#
#
# # def retrieve_by_query_parameters(*, session: Session, query_parameters: dict) -> Optional[List[Role]]:
# #     """Return list of role objects based on the given query parameters."""
# #
# #     statement = select(Role)
# #
# #     for attr, value in query_parameters.items():
# #         if value:
# #             statement = statement.filter(getattr(Role, attr).like(value))
# #
# #     retrieved_roles = session.exec(statement).all()
# #
# #     return retrieved_roles
# #
# #
# def update(*, session: Session, retrieved_result: Result, result: UpdateResultRequestModel) -> Optional[Result]:
#     """Updates an existing result object."""
#
#     retrieved_result.name = result.name
#     retrieved_result.total = result.total
#     retrieved_result.passed = result.passed
#     retrieved_result.failed = result.failed
#     retrieved_result.skipped = result.skipped
#     updated_result = retrieved_result
#
#     session.add(updated_result)
#     session.commit()
#     session.refresh(updated_result)
#
#     return updated_result
#
#
# def delete(*, session: Session, retrieved_result: Result) -> Optional[Result]:
#     """Deletes an existing result object."""
#
#     session.delete(retrieved_result)
#     session.commit()
#
#     return retrieved_result

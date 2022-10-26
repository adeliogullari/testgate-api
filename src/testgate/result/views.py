# from typing import List
# from sqlmodel import Session
# from fastapi import status, Depends, APIRouter, HTTPException
# from .service import create, retrieve_by_id, retrieve_by_name, delete
# from .schemas import CreateResultRequestModel, CreateResultResponseModel, DeleteResultResponseModel
# from ..user.views import allow_create_resource
# from ..database.database import get_session
#
# result_router = APIRouter(tags=["results"])
#
# ResultNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                         detail="A result with that id does not exist")
#
# ResultAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                              detail="A result with that id already exists")
#
#
# @result_router.get(path="/api/v1/result/{id}",
#                    response_model=None,
#                    status_code=200,
#                    dependencies=[Depends(allow_create_resource)])
# def retrieve_result_by_id(*, session: Session = Depends(get_session), id: int):
#     """Retrieve result by id."""
#
#     retrieved_role = retrieve_by_id(session=session, id=id)
#
#     if not retrieved_role:
#         raise ResultNotFoundException
#
#     return retrieved_role
#
#
# # @role_router.get(path="/api/v1/roles",
# #                  response_model=List[RetrieveRoleResponseModel],
# #                  status_code=200,
# #                  dependencies=[Depends(allow_create_resource)])
# # def retrieve_role_by_query_parameters(*, session: Session = Depends(get_session), name: str = None):
# #     """Search role by name."""
# #
# #     retrieved_role = retrieve_by_query_parameters(session=session, query_parameters={"name": name})
# #
# #     return retrieved_role
#
#
# @result_router.post(path="/api/v1/result",
#                     response_model=CreateResultResponseModel,
#                     status_code=201,
#                     dependencies=[Depends(allow_create_resource)])
# def create_result(*, session: Session = Depends(get_session), result: CreateResultRequestModel):
#     """Creates result."""
#
#     retrieved_result = retrieve_by_name(session=session, name=result.name)
#
#     if retrieved_result:
#         raise ResultAlreadyExistsException
#
#     created_result = create(session=session, result=result)
#
#     return created_result
#
#
# # @result_router.put(path="/api/v1/result/{id}",
# #                    response_model=UpdateRoleResponseModel,
# #                    status_code=200,
# #                    dependencies=[Depends(allow_create_resource)])
# # def update_role(*, session: Session = Depends(get_session), id: int, role: UpdateRoleRequestModel):
# #     """Updates role."""
# #
# #     retrieved_role = retrieve_by_id(session=session, id=id)
# #
# #     if not retrieved_role:
# #         raise RoleNotFoundException
# #
# #     updated_role = update(session=session, retrieved_role=retrieved_role, role=role)
# #
# #     return updated_role
# #
# #
# @result_router.delete(path="/api/v1/result/{id}",
#                       response_model=DeleteResultResponseModel,
#                       status_code=200,
#                       dependencies=[Depends(allow_create_resource)])
# def delete_result(*, session: Session = Depends(get_session), id: int):
#     """Deletes result."""
#
#     retrieved_result = retrieve_by_id(session=session, id=id)
#
#     if not retrieved_result:
#         raise ResultNotFoundException
#
#     deleted_result = delete(session=session, retrieved_result=retrieved_result)
#
#     return deleted_result

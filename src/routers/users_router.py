from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.user_model import UserModel
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserList, UserPublic, UserSchema
from src.services.user_service import UserService
from src.utils.misc import FilterPage
from src.utils.token import requires_admin

user_router = APIRouter(dependencies=[Depends(dependency=requires_admin)])

# INJECTIONS
T_Session = Annotated[AsyncSession, Depends(dependency=get_session)]


def user_service(session: T_Session) -> UserService:
    repo = UserRepository(session=session)
    return UserService(repository=repo)

T_FilterPage = Annotated[FilterPage, Query()]
T_Service = Annotated[UserService, Depends(dependency=user_service)]
T_Admin = Annotated[UserModel, Depends(dependency=requires_admin)]


# ========= CREATE ROUTER =========
@user_router.post(path="/", status_code=201, response_model=UserPublic)
async def create_user(service: T_Service, schema: UserSchema) -> UserModel:
    """
    Creates a new user.

    Args:
        service (UserService): The user service business logic.
        schema (UserSchema): The user data to create.

    Returns:
        UserModel: The created user record.
    """
    return await service.create(schema=schema)


# ========= READ ROUTER =========
@user_router.get(path="/", response_model=UserList)
async def list_users(service: T_Service, filter_page: T_FilterPage) -> dict[str, Sequence[UserModel]]:
    """
    Lists all users with pagination.

    Args:
        service (UserService): The user service business logic.
        filter_page (FilterPage): Pagination parameters (limit, offset).

    Returns:
        dict: A dictionary containing a list of users.
    """
    users: Sequence[UserModel] = await service.list(limit=filter_page.limit, offset=filter_page.offset)
    return {"users": users}


# ========= UPDATE ROUTER =========
@user_router.patch(path="/{user_id}", response_model=UserPublic)
async def update_user(service: T_Service, schema: UserSchema, user_id: int = Path()) -> UserModel:
    """
    Updates an existing user.

    Args:
        service (UserService): The user service business logic.
        schema (UserSchema): The user data to update.
        user_id (int): The ID of the user to update.

    Returns:
        UserModel: The updated user record.
    """
    return await service.update(schema=schema, user_id=user_id)


# ========= DELETE ROUTER =========
@user_router.delete(path="/{user_id}")
async def delete_user(service: T_Service, user_id: int = Path()) -> None:
    """
    Deletes a user.

    Args:
        service (UserService): The user service business logic.
        user_id (int): The ID of the user to delete.

    Returns:
        None
    """
    await service.delete(user_id=user_id)
    return None

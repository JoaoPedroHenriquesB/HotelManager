from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.user_model import UserModel
from src.schemas.user_schema import UserList, UserPublic, UserSchema
from src.services.user_service import UserService
from src.utils.misc import FilterPage
from src.utils.token import requires_admin

user_router = APIRouter(dependencies=[Depends(requires_admin)])

# INJECTIONS
T_Session = Annotated[AsyncSession, Depends(get_session)]
def user_service(session: T_Session) -> UserService:
    return UserService(session)

T_FilterPage = Annotated[FilterPage, Query()]
T_Service = Annotated[UserService, Depends(user_service)]
T_Admin = Annotated[UserModel, Depends(requires_admin)]


# ========= CREATE ROUTER =========
@user_router.post("/", status_code=201, response_model=UserPublic)
async def create_user(service: T_Service, schema: UserSchema) -> UserModel:
    return await service.create_user(schema)


# ========= READ ROUTER =========
@user_router.get("/", response_model=UserList)
async def list_users(
    service: T_Service, filter_page: T_FilterPage) -> dict[str, Sequence[UserModel]]:
    users = await service.list_users(filter_page.limit, filter_page.offset)
    return {"users": users}


# ========= UPDATE ROUTER =========
@user_router.patch("/{user_id}", response_model=UserPublic)
async def update_user(service: T_Service, schema: UserSchema, user_id: int = Path()) -> UserModel:
    return await service.update_user(schema, user_id)


# ========= DELETE ROUTER =========
@user_router.delete("/{user_id}")
async def delete_user(service: T_Service, user_id: int = Path()) -> None:
    await service.delete_user(user_id)
    return None

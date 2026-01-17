from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db_config import get_session
from src.models.guest_model import GuestModel
from src.models.user_model import UserModel
from src.schemas.guest_schema import GuestList, GuestPublic, GuestSchema
from src.services.guest_service import GuestService
from src.utils.misc import FilterPage
from src.utils.token import requires_admin

guest_router = APIRouter(dependencies=[Depends(requires_admin)])

# INJECTIONS
T_Session = Annotated[AsyncSession, Depends(get_session)]
def guest_service(session: T_Session) -> GuestService:
    return GuestService(session)

T_FilterPage = Annotated[FilterPage, Query()]
T_Service = Annotated[GuestService, Depends(guest_service)]
T_Admin = Annotated[UserModel, Depends(requires_admin)]


# ========= CREATE GUEST =========
@guest_router.post("/", response_model=GuestPublic, status_code=201)
async def create_guest(service: T_Service, schema: GuestSchema) -> GuestModel:
    return await service.create_guest(schema)


# ========= GET GUEST =========
@guest_router.get("/", response_model=GuestList)
async def list_guests(service: T_Service, filter_page: T_FilterPage) -> dict:
    guests = await service.list_guests(filter_page.limit, filter_page.offset)
    return {"guests": guests}


# ========= UPDATE GUEST =========
@guest_router.patch("/{guest_id}")
async def update_guest(service: T_Service, guest_id: int, schema: GuestSchema):
    return await service.update_guest(schema, guest_id)


# ========= DELETE GUEST =========
@guest_router.delete("/{guest_id}")
async def delete_guest(service: T_Service, guest_id: int):
    await service.delete_guest(guest_id)
    return None

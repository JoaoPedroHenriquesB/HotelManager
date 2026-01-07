from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db_config import get_session
from src.models.guest_model import GuestModel
from src.schemas.guest_schema import GuestList, GuestPublic, GuestSchema
from src.services.guest_service import GuestService
from src.utils.misc import FilterPage

user_router = APIRouter(prefix="/guest", tags=["Guests"])

# INJECTIONS
T_Session = Annotated[AsyncSession, Depends(get_session)]
def room_service(session: T_Session) -> GuestService:
  return GuestService(session)

T_FilterPage = Annotated[FilterPage, Query()]
T_Service = Annotated[GuestService, Depends(room_service)]


# CREATE NEW GUEST
@user_router.post("/create", response_model=GuestPublic, status_code=201)
async def create_guest(service: T_Service, schema: GuestSchema) -> GuestModel:
  return await service.create_guest(schema)


# LIST ALL GUESTS
@user_router.get("/list", response_model=GuestList)
async def list_guests(service: T_Service, filter_page: T_FilterPage) -> dict:
  guests = await service.list_guests(filter_page.limit, filter_page.offset)
  return {"guests": guests}


# UPDATE AN GUEST
@user_router.patch("/update")
async def update_guest(service: T_Service, guest_id: int, schema: GuestSchema):
  return await service.update_guest(schema, guest_id)


# DELETE AN USER
@user_router.delete("/delete")
async def delete_guest(service: T_Service, guest_id: int):
  return await service.delete_guest(guest_id)

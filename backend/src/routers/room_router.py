from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db_config import get_session
from src.models.room_model import RoomModel
from src.schemas.room_schema import RoomInternal, RoomList, RoomSchema
from src.services.room_services import RoomService

room_router = APIRouter(prefix="/room", tags=["Rooms"])

# INJECTIONS
T_Session = Annotated[AsyncSession, Depends(get_session)]
def room_service(session: T_Session) -> RoomService:
  return RoomService(session)

T_Service = Annotated[RoomService, Depends(room_service)]


#CREATE ROOM
@room_router.post("/create", response_model=RoomInternal, status_code=201)
async def create_room(service: T_Service, schema: RoomSchema) -> RoomModel:
  return await service.create_room(schema)


# GET ALL ROOMS
@room_router.get("/list", response_model=RoomList)
async def list_rooms(service: T_Service, limit: int, offset: int) -> dict:
  rooms = await service.list_rooms(limit, offset)
  return {"rooms": rooms}


# UPDATE ROOM
@room_router.patch("/update/{room_id}")
async def update_room(service: T_Service, room_id: int, schema: RoomSchema) -> RoomModel:
  return await service.update_room(schema, room_id)


# DELETE ROOM
@room_router.delete("/delete/{room_id}")
async def delete_room(service: T_Service, room_id: int) -> dict:
  return await service.delete_room(room_id)

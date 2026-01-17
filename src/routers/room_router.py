from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.room_model import RoomModel
from src.models.user_model import UserModel
from src.schemas.room_schema import RoomInternal, RoomList, RoomSchema
from src.services.room_service import RoomService
from src.utils.misc import FilterPage
from src.utils.token import requires_admin

room_router = APIRouter()

# INJECTIONS
T_Session = Annotated[AsyncSession, Depends(get_session)]
def room_service(session: T_Session) -> RoomService:
    return RoomService(session)

T_FilterPage = Annotated[FilterPage, Query()]
T_Service = Annotated[RoomService, Depends(room_service)]
T_Admin = Annotated[UserModel, Depends(requires_admin)]


# ========= CREATE ROOM =========
@room_router.post("/", response_model=RoomInternal, status_code=201)
async def create_room(service: T_Service, schema: RoomSchema) -> RoomModel:
    """Creates a new room.

    Args:
        service (RoomService): The room service business logic.
        schema (RoomSchema): The room data to create.

    Returns:
        RoomModel: The created room record.
    """
    return await service.create_room(schema)


# ========= GET ROOM =========
@room_router.get("/", response_model=RoomList)
async def list_rooms(service: T_Service, filter_page: T_FilterPage) -> dict:
    """Lists all rooms with pagination.

    Args:
        service (RoomService): The room service business logic.
        filter_page (FilterPage): Pagination parameters (limit, offset).

    Returns:
        dict: A dictionary containing a list of rooms.
    """
    rooms = await service.list_rooms(filter_page.limit, filter_page.offset)
    return {"rooms": rooms}


# ========= UPDATE ROOM =========
@room_router.patch("/{room_id}")
async def update_room(
    service: T_Service, room_id: int, schema: RoomSchema) -> RoomModel:
    """Updates an existing room.

    Args:
        service (RoomService): The room service business logic.
        room_id (int): The ID of the room to update.
        schema (RoomSchema): The room data to update.

    Returns:
        RoomModel: The updated room record.
    """
    return await service.update_room(schema, room_id)


# ========= DELETE ROOM =========
@room_router.delete("/{room_id}")
async def delete_room(service: T_Service, room_id: int):
    """Deletes a room.

    Args:
        service (RoomService): The room service business logic.
        room_id (int): The ID of the room to delete.

    Returns:
        None
    """
    await service.delete_room(room_id)
    return None

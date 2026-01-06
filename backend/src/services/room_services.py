import logging

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.room_model import RoomModel
from src.repositories.room_repository import RoomRepository
from src.utils.exceptions import NotFoundError
logger = logging.getLogger(__name__)

class RoomService:
  def __init__(self, session: AsyncSession) -> None:
    self.repository = RoomRepository(session)

  #CREATE NEW ROOM
  async def create_room(self, schema):

    new_room = RoomModel(
      room_number=schema.room_number,
      daily_value=schema.daily_value,
      room_type=schema.room_type
      )

    return await self.repository.create_room(new_room)


  # LIST ALL ROOMS
  async def list_rooms(self, limit: int, offset: int):
    rooms = await self.repository.get_rooms(limit, offset)

    if not rooms:
      raise NotFoundError()

    return rooms


  # UPDATE ROOM
  async def update_room(self, schema, room_id):
    db_room = await self.repository.get_room_id(room_id)

    if not db_room:
      raise NotFoundError()

    db_room.room_number = schema.room_number
    db_room.daily_value = schema.daily_value
    db_room.room_type = schema.room_type
    db_room.status = schema.status

    return await self.repository.update_room(db_room)


  # DELETE ROOM
  async def delete_room(self, room_id):
    db_room = await self.repository.get_room_id(room_id)

    if not db_room:
      raise NotFoundError()

    return await self.repository.delete_room(room_id)

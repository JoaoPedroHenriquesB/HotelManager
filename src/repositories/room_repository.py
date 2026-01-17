from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db_config import get_session
from src.models.room_model import RoomModel

T_Session = Annotated[AsyncSession, Depends(get_session)]

class RoomRepository:
  def __init__(self, session: T_Session) -> None:
    self.session = session


  # CREATE NEW ROOM
  async def create_room(self, room_model: RoomModel):
    try:
      self.session.add(room_model)
      await self.session.commit()
      await self.session.refresh(room_model)
      return room_model

    except SQLAlchemyError:
      await self.session.rollback()
      raise


  # LIST ALL ROOMS
  async def get_rooms(self, limit: int, offset: int):
    result = await self.session.scalars(select(RoomModel).limit(limit).offset(offset))
    return result.all()

  # GET ROOM BY ID
  async def get_by_id(self, room_id):
    return await self.session.scalar(select(RoomModel).where(RoomModel.id == room_id))


  # UPDATE ROOM
  async def update_room(self, room_model: RoomModel):
    try:
      self.session.add(room_model)
      await self.session.commit()
      await self.session.refresh(room_model)
      return room_model

    except SQLAlchemyError:
      await self.session.rollback()
      raise


  # DELETE ROOM
  async def delete_room(self, room_id):
    try:
      room_to_delete = await self.session.get(RoomModel, room_id)
      await self.session.delete(room_to_delete)
      await self.session.commit()
      return {"message": f"room id {room_id}, deleted!"}

    except SQLAlchemyError:
      await self.session.rollback()
      raise

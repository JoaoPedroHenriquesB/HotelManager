from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.guest_model import GuestModel

T_Session = Annotated[AsyncSession, Depends(get_session)]

class GuestRepository:
  def __init__(self, session: T_Session) -> None:
    self.session = session

  async def get_by_id(self, guest_id: int):
    return await self.session.scalar(select(GuestModel).where(GuestModel.id == guest_id))

  async def verify_data(self, guest_cpf: str):
    return await self.session.scalar(select(GuestModel).where(GuestModel.cpf ==guest_cpf))


  async def create_guest(self, guest_model: GuestModel):
    try:
      self.session.add(guest_model)
      await self.session.commit()
      await self.session.refresh(guest_model)
      return guest_model

    except SQLAlchemyError:
      await self.session.rollback()
      raise


  async def get_guests(self, limit, offset):
      result = await self.session.scalars(select(GuestModel).limit(limit).offset(offset))
      return result.all()


  async def update_guest(self, guest_model: GuestModel):
    try:
      self.session.add(guest_model)
      await self.session.commit()
      await self.session.refresh(guest_model)
      return guest_model

    except SQLAlchemyError:
      await self.session.rollback()
      raise


  async def delete_guest(self, guest_id):
    try:
      guest_to_delete = await self.session.get(GuestModel, guest_id)
      await self.session.delete(guest_to_delete)
      await self.session.commit()

    except SQLAlchemyError:
      await self.session.rollback()
      raise

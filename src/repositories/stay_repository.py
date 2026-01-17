from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_session
from src.models.stay_model import StayModel, StayStatus

T_Session = Annotated[AsyncSession, Depends(get_session)]

class StayRepository:
  def __init__(self, session: T_Session) -> None:
    self.session = session

  # GET STAY BY ID
  async def get_by_id(self, guest_id: int):
    return await self.session.scalar(select(StayModel).where(StayModel.guest_id == guest_id, StayModel.status == StayStatus.ACTIVE))


# ACTIVE STAY BY GUEST
  async def get_active_stay_by_guest_id(self, guest_id: int):
    query = (select(StayModel).where(StayModel.guest_id == guest_id,StayModel.status == StayStatus.ACTIVE))
    return await self.session.scalar(query)


  # CREATE NEW STAY
  async def create_stay(self, stay_model: StayModel):
    try:
      self.session.add(stay_model)
      await self.session.commit()
      await self.session.refresh(stay_model)
      return stay_model

    except SQLAlchemyError:
      await self.session.rollback()
      raise


  # UPDATE STAY
  async def update_stay(self, stay_model: StayModel):
    try:
      self.session.add(stay_model)
      await self.session.commit()
      await self.session.refresh(stay_model)
      return stay_model

    except SQLAlchemyError:
      await self.session.rollback()
      raise


  # LIST ALL STAYS
  async def list_stays(self, limit: int, offset: int):
      stays = await self.session.scalars(select(StayModel).limit(limit).offset(offset))
      return stays.all()


  # LIST ALL ACTIVES STAYS
  async def active_stays(self, limit: int, offset: int):
      stays = await self.session.scalars(select(StayModel).where(StayModel.status == StayStatus.ACTIVE).limit(limit).offset(offset))
      return stays.all()

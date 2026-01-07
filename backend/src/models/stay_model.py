from enum import Enum
from datetime import datetime
from src.database.db_config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as SQLEnum
from src.models.room_model import RoomModel
from src.models.guest_model import GuestModel

class StayStatus(Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    FINISHED = "finished"

class StayModel(Base):
  __tablename__ = "stays"

  #room: Mapped["RoomModel"] = relationship(back_populates="stays")
  #guest: Mapped["GuestModel"] = relationship(back_populates="stays")

  id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
  room_number: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
  guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"))
  check_in_date: Mapped[datetime] = mapped_column(nullable=False)
  check_out_date: Mapped[datetime] = mapped_column(nullable=False)
  status: Mapped[StayStatus] = mapped_column(SQLEnum(StayStatus), default=StayStatus.SCHEDULED, nullable=False)

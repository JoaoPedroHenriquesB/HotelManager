from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db_config import Base


class StayStatus(Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    FINISHED = "finished"

class StayModel(Base):
  __tablename__ = "stays"

  id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
  room_number: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
  guest_id: Mapped[int] = mapped_column(ForeignKey("guests.id"))
  check_in_date: Mapped[datetime] = mapped_column(nullable=False)
  check_out_date: Mapped[datetime] = mapped_column(nullable=False)
  status: Mapped[StayStatus] = mapped_column(SQLEnum(StayStatus), default=StayStatus.SCHEDULED, nullable=False)

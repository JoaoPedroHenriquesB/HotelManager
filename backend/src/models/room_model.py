from enum import Enum

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from src.database.db_config import Base


class RoomStatus(str, Enum):
    AVAILABLE = "avaliable"
    OCCUPIED = "occupied"
    DIRTY = "dirty"


class RoomType(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SUIT = "suit"

class RoomModel(Base):
  __tablename__ = "rooms"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)

  room_number: Mapped[int] = mapped_column(unique=True)
  daily_price: Mapped[float]
  room_type: Mapped[RoomType]
  status: Mapped[RoomStatus] = mapped_column(default="avaliable", init=True, server_default=text("'avaliable'"))

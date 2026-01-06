from typing import Literal

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from src.database.db_config import Base


class RoomModel(Base):
  __tablename__ = "rooms"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)

  room_number: Mapped[int] = mapped_column(unique=True)
  daily_value: Mapped[float]
  room_type: Mapped[Literal["single", "double", "suit"]]
  status: Mapped[Literal["avaliable", "unavailable", "maintenance"]] = mapped_column(default="avaliable", init=True, server_default=text("'avaliable'"))

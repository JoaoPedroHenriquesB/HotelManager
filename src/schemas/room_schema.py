from pydantic import BaseModel, ConfigDict
from src.models.room_model import RoomStatus, RoomType


class RoomSchema(BaseModel):
  room_number: int
  daily_price: float
  room_type: RoomType
  status: RoomStatus

class RoomInternal(RoomSchema):
  id: int

  model_config = ConfigDict(from_attributes=True)

class RoomList(BaseModel):
  rooms: list[RoomInternal]

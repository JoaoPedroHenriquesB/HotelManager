from typing import Literal

from pydantic import BaseModel, ConfigDict


class RoomSchema(BaseModel):
  room_number: int
  daily_value: float
  room_type: Literal["single", "double", "suit"]
  status: Literal["avaliable", "unavailable", "maintenance"]

class RoomInternal(RoomSchema):
  id: int

  model_config = ConfigDict(from_attributes=True)

class RoomList(BaseModel):
  rooms: list[RoomInternal]

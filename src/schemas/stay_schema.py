from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.models.stay_model import StayStatus

class StaySchema(BaseModel):
  guest_id: int
  room_number: int
  check_in_date: datetime
  check_out_date: datetime


class StayInternal(StaySchema):
  id: int
  status: StayStatus

  model_config = ConfigDict(from_attributes=True)

class StayCheckout(StaySchema):
  total_price: float
  status: StayStatus

  model_config = ConfigDict(from_attributes=True)


class StayList(BaseModel):
  stays: list[StayInternal]

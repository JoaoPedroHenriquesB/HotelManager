from pydantic import BaseModel, ConfigDict


class GuestSchema(BaseModel):
  name: str
  phone_number: str
  cpf: str
  room_number: int


class GuestPublic(BaseModel):
  id: int
  name: str
  phone_number: str
  room_number: int

  model_config = ConfigDict(from_attributes=True)

class GuestList(BaseModel):
  guests: list[GuestPublic]

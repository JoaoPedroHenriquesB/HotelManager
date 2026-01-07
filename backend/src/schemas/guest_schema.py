from pydantic import BaseModel, ConfigDict


class GuestSchema(BaseModel):
  name: str
  phone_number: str
  cpf: str


class GuestPublic(GuestSchema):
  id: int

  model_config = ConfigDict(from_attributes=True)

class GuestList(BaseModel):
  guests: list[GuestPublic]

from pydantic import BaseModel, Field

class FilterPage(BaseModel):
  limit: int = Field(ge=1, default=100)
  offset: int = Field(ge=0, default=0)

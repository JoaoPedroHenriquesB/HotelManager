from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: bool = False


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str

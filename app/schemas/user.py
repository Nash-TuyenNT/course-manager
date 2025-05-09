from pydantic import BaseModel

from app.enums.roles import Roles


class UserBase(BaseModel):
    username: str
    email: str
    role: Roles


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class SimpleUserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

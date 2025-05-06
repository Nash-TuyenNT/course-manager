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
        orm_mode = True


class SimpleUserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

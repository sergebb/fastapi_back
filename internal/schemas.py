from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ChatroomBase(BaseModel):
    name: str


class ChatroomCreate(ChatroomBase):
    pass


class Chatroom(ChatroomBase):
    id: int
    owner_id: int
    members: list[User] = []

    class Config:
        orm_mode = True

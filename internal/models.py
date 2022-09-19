from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    chatrooms = relationship("Chatroom", back_populates="owner")


userrooms_table = Table(
    "userrooms",
    Base.metadata,
    Column("user", ForeignKey("users.id")),
    Column("chatroom", ForeignKey("chatrooms.id")),
)


class Chatroom(Base):
    __tablename__ = "chatrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="chatrooms")
    members = relationship("User", secondary=userrooms_table)

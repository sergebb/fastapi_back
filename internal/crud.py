from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, username: str):
    return db.query(models.User).filter_by(username=username).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_chatrooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chatroom).offset(skip).limit(limit).all()


def get_chatroom(db: Session, name: str):
    return db.query(models.Chatroom).filter_by(name=name).first()


def create_chatroom(db: Session, chatroom: schemas.ChatroomCreate, user: schemas.User):
    db_chatroom = models.Chatroom(**chatroom.dict(), owner_id=user.id)
    db.add(db_chatroom)
    db.commit()
    db.refresh(db_chatroom)
    return db_chatroom

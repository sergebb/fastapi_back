from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from internal import schemas, crud, auth
from internal.database import get_session


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/users/", response_model=list[schemas.User])
async def get_users(skip: int = 0, limit: int = 100,
        current_user: schemas.User = Depends(auth.get_current_active_user),
        db: Session = Depends(get_session)):
    return crud.get_users(db, skip, limit)


@router.get("/users/{username}", response_model=schemas.User)
async def get_users(username: str,
        current_user: schemas.User = Depends(auth.get_current_active_user),
        db: Session = Depends(get_session)):
    user = crud.get_user(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.post("/users/", response_model=schemas.User)
async def post_users(user: schemas.UserCreate, db: Session = Depends(get_session)):
    hashed_password = auth.get_password_hash(user.password)
    try:
        user = crud.create_user(db, user, hashed_password)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflict username or email",
        )
    
    return user


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    print(current_user)
    return current_user


@router.post("/token/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}

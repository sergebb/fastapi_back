from starlette.concurrency import run_until_first_complete

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from internal import auth, broadcast, crud, schemas
from internal.database import get_session


router = APIRouter(prefix="/api/v1.0/chatroom", tags=["chatroom"])


@router.get("/", response_model=list[schemas.Chatroom])
async def get_chatrooms(skip: int = 0, limit: int = 100,
        current_user: schemas.User = Depends(auth.get_current_active_user),
        db: Session = Depends(get_session)):
    return crud.get_chatrooms(db, skip, limit)


@router.post("/", response_model=schemas.Chatroom)
async def post_chatrooms(chatroom: schemas.ChatroomCreate,
        current_user: schemas.User = Depends(auth.get_current_active_user),
        db: Session = Depends(get_session)):
    try:
        chatroom = crud.create_chatroom(db, chatroom, current_user)
    except IntegrityError as e:
        if 'email' in e.orig.diag.message_detail:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                email="Email already exists",
            )
        if 'username' in e.orig.diag.message_detail:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                username="Email already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Integrity error: {e.orig.diag.message_detail}",
        )
        
    
    return chatroom


@router.get("/{name}", response_model=schemas.Chatroom)
async def get_chatroom(name: str,
        current_user: schemas.User = Depends(auth.get_current_active_user),
        db: Session = Depends(get_session)):
    chatroom = crud.get_chatroom(db, name)
    if chatroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatroom not found",
        )

    return chatroom


@router.websocket("/{chatname}/ws")
async def websocket_endpoint(websocket: WebSocket, chatname: str, db: Session = Depends(get_session)):
    await websocket.accept()
    auth_data = await websocket.receive_text()
    if not auth_data.startswith('Bearer '):
        websocket.close()
    
    user = auth.get_user_from_token(db, auth_data[7:])

    await run_until_first_complete(
        (broadcast.ws_receiver, {"websocket": websocket, 'chatname': chatname, 'username': user.username}),
        (broadcast.ws_sender, {"websocket": websocket, 'chatname': chatname}),
    )

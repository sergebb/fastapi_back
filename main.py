from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, chatrooms
from internal import models
from internal.broadcast import broadcast
from internal.database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    on_startup=[broadcast.connect],
    on_shutdown=[broadcast.disconnect]
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chatrooms.router)

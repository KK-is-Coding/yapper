from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db
from app.cleanup import cleanup_rooms
from app.api.rooms import router as rooms_router
from app.api.media import router as media_router
from app.websocket import router as websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    cleanup_rooms()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Yapper backend running"}


app.include_router(rooms_router)
app.include_router(media_router)
app.include_router(websocket_router)

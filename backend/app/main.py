from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app_archive.database import create_db_and_tables
from app.api.v1 import rooms
from app.websocket.handlers import handle_websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("✅ Database initialized")
    yield
    print("👋 Shutting down")


app = FastAPI(
    title="Yapper API",
    description="Location-based anonymous chat application",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ONLY ROOMS API (no auth, no messages REST)
app.include_router(rooms.router, prefix="/api/v1")


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await handle_websocket(websocket, room_id)


@app.get("/")
def root():
    return {"message": "Yapper API running"}

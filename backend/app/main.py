from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import create_db_and_tables
from app.api.v1 import auth, rooms, messages
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

# ✅ FIXED CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await handle_websocket(websocket, room_id)


@app.get("/")
def root():
    return {"message": "Yapper API is running", "version": "1.0.0"}

from fastapi import APIRouter, WebSocket
from app.ws.handlers import chat_handler

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await chat_handler(websocket, room_id)

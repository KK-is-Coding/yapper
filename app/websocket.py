from fastapi import APIRouter, WebSocket
from app.ws.handlers import chat_handler

# WebSocket router
router = APIRouter()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """
    WebSocket entrypoint for a chat room.
    This function should NEVER contain business logic.
    """
    await chat_handler(websocket, room_id)

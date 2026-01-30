from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session
import json

from app.websocket.connection_manager import manager
from app.database import engine
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate


async def handle_websocket(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)

    try:
        join_raw = await websocket.receive_text()
        join_data = json.loads(join_raw)

        if join_data.get("type") != "join":
            await websocket.close()
            return

        username = join_data.get("nickname")
        client_id = join_data.get("client_id")

        if not username or not client_id:
            await websocket.close()
            return

        if manager.is_client_in_other_room(client_id, room_id):
            await websocket.send_json({
                "type": "error",
                "message": "You are already connected to another room"
            })
            await websocket.close()
            return

        manager.register_client(client_id, room_id, websocket)

        with Session(engine) as db:
            history = MessageService.get_room_messages(room_id, db)
            for msg in history:
                await websocket.send_json({
                    "type": "message",
                    "id": msg.id,
                    "sender": msg.username,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                })

        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            if data.get("type") != "message":
                continue

            content = data.get("content")
            if not content:
                continue

            with Session(engine) as db:
                saved = MessageService.create_message(
                    room_id=room_id,
                    username=username,
                    message_data=MessageCreate(content=content),
                    db=db
                )

            await manager.broadcast(room_id, {
                "type": "message",
                "id": saved.id,
                "sender": saved.username,
                "content": saved.content,
                "timestamp": saved.timestamp
            })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session
import json

from app.websocket.connection_manager import manager
from app_archive.database import engine
from app_archive.services.message_service import MessageService
from app_archive.services.room_service import RoomService
from app.schemas.message import MessageCreate


async def handle_websocket(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)

    try:
        join_data = json.loads(await websocket.receive_text())
        username = join_data.get("nickname")

        if not username:
            await websocket.close()
            return

        with Session(engine) as db:
            RoomService.get_room_by_id(room_id, db)
            history = MessageService.get_room_messages(room_id, db)
            for msg in history:
                await websocket.send_json({
                    "id": msg.id,
                    "sender": msg.username,
                    "text": msg.content,
                    "timestamp": msg.timestamp
                })

        while True:
            data = json.loads(await websocket.receive_text())
            content = data.get("content")

            if not content:
                continue

            with Session(engine) as db:
                msg = MessageService.create_message(
                    room_id,
                    username,
                    MessageCreate(content=content),
                    db
                )

            await manager.broadcast(room_id, {
                "id": msg.id,
                "sender": msg.username,
                "text": msg.content,
                "timestamp": msg.timestamp
            })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

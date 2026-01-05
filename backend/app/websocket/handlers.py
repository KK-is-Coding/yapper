from fastapi import WebSocket, WebSocketDisconnect
from sqlmodel import Session
import json
from datetime import datetime, timezone

from app.websocket.connection_manager import manager
from app.database import engine
from app.core.security import decode_access_token
from app.services.message_service import MessageService
from app.services.room_service import RoomService
from app.models.user import User
from app.schemas.message import MessageCreate


async def handle_websocket(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)

    try:
        # 🔐 AUTH MESSAGE
        auth_data = await websocket.receive_text()
        auth_json = json.loads(auth_data)

        token = auth_json.get("token")
        if not token:
            await websocket.close()
            return

        payload = decode_access_token(token)
        if not payload:
            await websocket.close()
            return

        user_id = payload["sub"]
        username = payload["username"]

        with Session(engine) as db:
            user = db.get(User, user_id)
            RoomService.get_room_by_id(room_id, db)

            # ✅ SEND HISTORY (frontend shape)
            messages = MessageService.get_room_messages(room_id, db)
            for msg in messages:
                await websocket.send_json({
                    "id": msg.id,
                    "sender": msg.username,
                    "text": msg.content,
                    "timestamp": datetime.fromisoformat(msg.timestamp)
                    .strftime("%I:%M %p")
                })

        # 🔁 MESSAGE LOOP
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            content = data.get("content")
            if not content:
                continue

            with Session(engine) as db:
                msg = MessageService.create_message(
                    room_id,
                    user_id,
                    username,
                    MessageCreate(content=content),
                    db
                )

            await manager.broadcast(room_id, {
                "id": msg.id,
                "sender": msg.username,
                "text": msg.content,
                "timestamp": datetime.fromisoformat(msg.timestamp)
                .strftime("%I:%M %p")
            })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

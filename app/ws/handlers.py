from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError

from app.ws.manager import ConnectionManager
from app.ws.validator import validate_join
from app.services.message_service import save_message, load_recent_messages
from app.auth.security import decode_token
from app.database import engine
from app.models import User
from sqlmodel import Session
import json

manager = ConnectionManager()


async def chat_handler(websocket: WebSocket, room_id: str):
    await websocket.accept()

    try:
        # -------- JOIN MESSAGE --------
        join_raw = await websocket.receive_text()
        join = json.loads(join_raw)

        token = join.get("token")
        lat = join.get("lat")
        lon = join.get("lon")

        if not token:
            await websocket.send_json({"error": "Missing token"})
            await websocket.close()
            return

        # -------- JWT VALIDATION --------
        try:
            payload = decode_token(token)
            user_id = payload.get("sub")
            if not user_id:
                raise ValueError("Invalid token")
        except (JWTError, ValueError):
            await websocket.send_json({"error": "Invalid token"})
            await websocket.close()
            return

        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user:
                await websocket.send_json({"error": "User not found"})
                await websocket.close()
                return

        username = user.username

        # -------- LOCATION VALIDATION --------
        ok, result = validate_join(room_id, lat, lon)
        if not ok:
            await websocket.send_json({"error": result})
            await websocket.close()
            return

        # -------- SEND CHAT HISTORY --------
        for msg in reversed(load_recent_messages(room_id)):
            await websocket.send_json({
                "type": msg.type,
                "user": msg.user_id,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            })

        manager.connect(room_id, websocket)

        # -------- MESSAGE LOOP --------
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            if "type" not in data or "content" not in data:
                continue

            msg = save_message(
                room_id=room_id,
                user_id=username,   # 👈 username, not random id
                msg_type=data["type"],
                content=data["content"]
            )

            await manager.broadcast(room_id, {
                "type": msg.type,
                "user": username,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

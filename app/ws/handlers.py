from fastapi import WebSocket, WebSocketDisconnect
from app.ws.manager import ConnectionManager
from app.ws.validator import validate_join
from app.services.message_service import save_message, load_recent_messages

manager = ConnectionManager()

async def chat_handler(websocket: WebSocket, room_id: str):
    await websocket.accept()

    # --- JOIN PHASE ---
    join = await websocket.receive_json()
    ok, result = validate_join(room_id, join["lat"], join["lon"])

    if not ok:
        await websocket.send_json({"error": result})
        await websocket.close()
        return

    user_id = join["user_id"]

    # --- SEND CHAT HISTORY ---
    for msg in reversed(load_recent_messages(room_id)):
        await websocket.send_json({
            "type": msg.type,
            "user_id": msg.user_id,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
        })

    manager.connect(room_id, websocket)

    # --- MESSAGE LOOP (CRITICAL FIX HERE) ---
    try:
        while True:
            data = await websocket.receive_json()

            # Validate incoming message
            if "type" not in data or "content" not in data:
                continue  # ignore malformed messages

            msg = save_message(
                room_id,
                user_id,
                data["type"],
                data["content"],
            )

            await manager.broadcast(room_id, {
                "type": msg.type,
                "user_id": msg.user_id,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            })

    except WebSocketDisconnect:
        # REAL disconnect (tab closed, network lost)
        manager.disconnect(room_id, websocket)

    except Exception as e:
        # 🔥 THIS WAS MISSING
        print("WebSocket error:", e)
        manager.disconnect(room_id, websocket)
        await websocket.close()

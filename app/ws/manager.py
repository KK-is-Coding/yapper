from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}

    def connect(self, room_id: str, websocket: WebSocket):
        self.connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.connections[room_id].remove(websocket)
        if not self.connections[room_id]:
            del self.connections[room_id]

    async def broadcast(self, room_id: str, message: dict):
        for ws in self.connections.get(room_id, []):
            await ws.send_json(message)

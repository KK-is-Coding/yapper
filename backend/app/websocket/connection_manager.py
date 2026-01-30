from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.client_rooms: Dict[str, str] = {}
        self.socket_clients: Dict[WebSocket, str] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = []

        self.active_connections[room_id].append(websocket)

    def register_client(self, client_id: str, room_id: str, websocket: WebSocket):
        self.client_rooms[client_id] = room_id
        self.socket_clients[websocket] = client_id

    def is_client_in_other_room(self, client_id: str, room_id: str) -> bool:
        return client_id in self.client_rooms and self.client_rooms[client_id] != room_id

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)

            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

        client_id = self.socket_clients.pop(websocket, None)
        if client_id:
            self.client_rooms.pop(client_id, None)

    async def broadcast(self, room_id: str, message: dict):
        if room_id not in self.active_connections:
            return

        for connection in self.active_connections[room_id]:
            await connection.send_json(message)


manager = ConnectionManager()

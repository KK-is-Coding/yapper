from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import rooms, messages
from app.websocket.handlers import handle_websocket
from app.database import init_db

app = FastAPI(title="Yapper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")

app.add_api_websocket_route(
    "/ws/{room_id}",
    handle_websocket
)


@app.on_event("startup")
def on_startup():
    init_db()

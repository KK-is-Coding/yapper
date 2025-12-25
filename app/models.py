from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid


# -------------------- USER (JWT) --------------------

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str


# -------------------- CHAT ROOM --------------------

class ChatRoom(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    latitude: float
    longitude: float

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=2)
    )

    is_active: bool = True


# -------------------- MESSAGE --------------------

class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    room_id: str = Field(index=True)
    user_id: str
    type: str
    content: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

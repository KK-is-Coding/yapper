from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
import uuid


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    room_id: str = Field(index=True, foreign_key="rooms.id")
    user_id: str = Field(index=True)
    username: str  # Denormalized for faster queries

    # Content
    content: str = Field(max_length=300)

    # Timestamp
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

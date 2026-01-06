from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    room_id: str = Field(index=True)
    username: str
    content: str = Field(max_length=300)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

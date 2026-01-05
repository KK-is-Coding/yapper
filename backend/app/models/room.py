from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid


class Room(SQLModel, table=True):
    __tablename__ = "rooms"

    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=50)
    creator_id: str = Field(index=True)

    # Location
    latitude: float
    longitude: float

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=2)
    )

    # Status
    is_active: bool = True

from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta, timezone
import uuid


class Room(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    name: str
    latitude: float
    longitude: float
    is_active: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=2)
    )

from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    username: str = Field(unique=True, index=True, min_length=3, max_length=50)
    hashed_password: str
    created_at: Optional[str] = None  # ISO format timestamp

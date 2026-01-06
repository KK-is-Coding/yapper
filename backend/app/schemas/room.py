from pydantic import BaseModel, Field
from typing import Optional


class RoomCreate(BaseModel):
    name: str = Field(max_length=50)
    latitude: float
    longitude: float


class RoomResponse(BaseModel):
    id: str
    name: str
    location: str
    latitude: float
    longitude: float
    created_at: str
    expires_at: str
    is_active: bool

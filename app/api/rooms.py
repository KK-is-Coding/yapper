from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime, timezone
from typing import List

from app.database import engine
from app.models import ChatRoom
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])


# -------------------------------------------------
# Helper: simple distance check (~5km)
# -------------------------------------------------
def is_within_range(lat1: float, lon1: float, lat2: float, lon2: float) -> bool:
    """
    Very simple distance approximation.
    ~0.05 degrees ≈ 5km (good enough for MVP).
    """
    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2
    distance = (lat_diff * lat_diff + lon_diff * lon_diff) ** 0.5
    return distance <= 0.05


# -------------------------------------------------
# Create Room (JWT protected)
# -------------------------------------------------
@router.post("/create")
def create_room(
    lat: float,
    lon: float,
    user=Depends(get_current_user)
):
    with Session(engine) as session:
        room = ChatRoom(
            latitude=lat,
            longitude=lon
        )
        session.add(room)
        session.commit()
        session.refresh(room)

        return {
            "id": room.id,
            "latitude": room.latitude,
            "longitude": room.longitude,
            "created_at": room.created_at.isoformat(),
            "expires_at": room.expires_at.isoformat(),
            "is_active": room.is_active
        }


# -------------------------------------------------
# Find Nearby Rooms (PUBLIC)
# -------------------------------------------------
@router.get("/nearby", response_model=List[ChatRoom])
def nearby_rooms(lat: float, lon: float):
    """
    Returns all active, non-expired rooms within ~5km range.
    """

    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        rooms = session.exec(select(ChatRoom)).all()

    nearby: List[ChatRoom] = []

    for room in rooms:
        # ---- timezone safety ----
        expires_at = room.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        # ---- filters ----
        if not room.is_active:
            continue

        if expires_at <= now:
            continue

        if not is_within_range(
            lat, lon,
            room.latitude, room.longitude
        ):
            continue

        nearby.append(room)

    return nearby

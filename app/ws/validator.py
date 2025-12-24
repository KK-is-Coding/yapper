from datetime import datetime, timezone
from sqlmodel import Session

from app.database import engine
from app.models import ChatRoom
from app.geo import distance_km
from app.utils.time import ensure_utc


def validate_join(room_id: str, lat: float, lon: float):
    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        room = session.get(ChatRoom, room_id)

        if not room:
            return False, "Room not found"

        if ensure_utc(room.expires_at) <= now:
            return False, "Room expired"

        if distance_km(lat, lon, room.latitude, room.longitude) > 5:
            return False, "Too far from room"

        return True, room

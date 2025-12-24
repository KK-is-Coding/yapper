from fastapi import APIRouter
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.database import engine
from app.models import ChatRoom
from app.geo import distance_km
from app.utils.time import ensure_utc


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/create")
def create_room(lat: float, lon: float):
    room = ChatRoom(latitude=lat, longitude=lon)
    with Session(engine) as session:
        session.add(room)
        session.commit()
        session.refresh(room)
    return room


@router.get("/nearby")
def nearby_rooms(lat: float, lon: float):
    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        rooms = session.exec(
            select(ChatRoom).where(ChatRoom.is_active == True)
        ).all()

    return [
        room for room in rooms
        if ensure_utc(room.expires_at) > now
        and distance_km(lat, lon, room.latitude, room.longitude) <= 5
    ]

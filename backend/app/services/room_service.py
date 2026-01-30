from sqlmodel import Session, select
from datetime import datetime
from typing import List

from app.models.room import Room
from app.schemas.room import RoomCreate, RoomResponse
from app.core.geo import is_within_range


class RoomService:

    @staticmethod
    def create_room(room_data: RoomCreate, db: Session) -> RoomResponse:
        room = Room(
            name=room_data.name,
            latitude=room_data.latitude,
            longitude=room_data.longitude
        )

        db.add(room)
        db.commit()
        db.refresh(room)

        return RoomResponse(
            id=room.id,
            name=room.name,
            location=f"{room.latitude:.4f}, {room.longitude:.4f}",
            latitude=room.latitude,
            longitude=room.longitude,
            created_at=room.created_at.isoformat(),
            expires_at=room.expires_at.isoformat(),
            is_active=room.is_active
        )

    @staticmethod
    def get_nearby_rooms(lat: float, lon: float, db: Session) -> List[RoomResponse]:
        now = datetime.utcnow()

        rooms = db.exec(
            select(Room).where(Room.is_active == True)
        ).all()

        nearby: List[RoomResponse] = []

        for room in rooms:
            if room.expires_at <= now:
                room.is_active = False
                db.add(room)
                continue

            if is_within_range(lat, lon, room.latitude, room.longitude):
                nearby.append(
                    RoomResponse(
                        id=room.id,
                        name=room.name,
                        location=f"{room.latitude:.4f}, {room.longitude:.4f}",
                        latitude=room.latitude,
                        longitude=room.longitude,
                        created_at=room.created_at.isoformat(),
                        expires_at=room.expires_at.isoformat(),
                        is_active=room.is_active
                    )
                )

        db.commit()
        return nearby

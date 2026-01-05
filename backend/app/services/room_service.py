from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import datetime, timezone
from typing import List

from app.models.room import Room
from app.models.user import User
from app.schemas.room import RoomCreate, RoomResponse
from app.core.geo import is_within_range


class RoomService:
    @staticmethod
    def create_room(room_data: RoomCreate, user: User, db: Session) -> RoomResponse:
        new_room = Room(
            name=room_data.name,
            creator_id=user.id,
            latitude=room_data.latitude,
            longitude=room_data.longitude
        )

        db.add(new_room)
        db.commit()
        db.refresh(new_room)

        return RoomResponse(
            id=new_room.id,
            name=new_room.name,
            location=f"{new_room.latitude:.4f}, {new_room.longitude:.4f}",
            latitude=new_room.latitude,
            longitude=new_room.longitude,
            created_at=new_room.created_at.isoformat(),
            expires_at=new_room.expires_at.isoformat(),
            is_active=new_room.is_active
        )

    @staticmethod
    def get_nearby_rooms(lat: float, lon: float, db: Session) -> List[RoomResponse]:
        now = datetime.now(timezone.utc)

        # Get all active rooms
        rooms = db.exec(
            select(Room).where(Room.is_active == True)
        ).all()

        nearby_rooms = []
        for room in rooms:
            # Check if expired
            expires_at = room.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)

            if expires_at <= now:
                room.is_active = False
                db.add(room)
                continue

            # Check if within range
            if is_within_range(lat, lon, room.latitude, room.longitude):
                nearby_rooms.append(RoomResponse(
                    id=room.id,
                    name=room.name,
                    location=f"{room.latitude:.4f}, {room.longitude:.4f}",
                    latitude=room.latitude,
                    longitude=room.longitude,
                    created_at=room.created_at.isoformat(),
                    expires_at=room.expires_at.isoformat(),
                    is_active=room.is_active
                ))

        db.commit()
        return nearby_rooms

    @staticmethod
    def get_room_by_id(room_id: str, db: Session) -> Room:
        room = db.get(Room, room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        return room

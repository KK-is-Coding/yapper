from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.room import RoomCreate, RoomResponse
from app.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room(
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat room"""
    return RoomService.create_room(room_data, current_user, db)


@router.get("/nearby", response_model=List[RoomResponse])
def get_nearby_rooms(
    lat: float = Query(..., description="User latitude"),
    lon: float = Query(..., description="User longitude"),
    db: Session = Depends(get_db)
):
    """Get all nearby active rooms within 5km"""
    return RoomService.get_nearby_rooms(lat, lon, db)

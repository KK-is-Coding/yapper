from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List

from app_archive.database import get_session
from app.schemas.room import RoomCreate, RoomResponse
from app_archive.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_session)
):
    return RoomService.create_room(room_data, db)


@router.get("/nearby", response_model=List[RoomResponse])
def get_nearby_rooms(
    lat: float = Query(...),
    lon: float = Query(...),
    db: Session = Depends(get_session)
):
    return RoomService.get_nearby_rooms(lat, lon, db)

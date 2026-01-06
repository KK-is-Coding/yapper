from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app_archive.models.user import User
from app.schemas.message import MessageCreate, MessageResponse
from app_archive.services.message_service import MessageService

router = APIRouter(prefix="/rooms/{room_id}/messages", tags=["Messages"])


@router.get("/", response_model=List[MessageResponse])
def get_messages(
    room_id: str,
    db: Session = Depends(get_db)
):
    """Get all messages in a room"""
    return MessageService.get_room_messages(room_id, db)


@router.post("/", response_model=MessageResponse, status_code=201)
def send_message(
    room_id: str,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to a room"""
    return MessageService.create_message(
        room_id,
        current_user.id,
        current_user.username,
        message_data,
        db
    )

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.api.deps import get_db
from app.schemas.message import MessageResponse
from app.services.message_service import MessageService

router = APIRouter(
    prefix="/rooms/{room_id}/messages",
    tags=["Messages"]
)


@router.get("/", response_model=List[MessageResponse])
def get_messages(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Get message history for a room.
    Messages are sent via WebSocket, not REST.
    """
    return MessageService.get_room_messages(room_id, db)

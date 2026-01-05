from sqlmodel import Session, select
from typing import List
from datetime import datetime, timezone

from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse


class MessageService:
    @staticmethod
    def create_message(
        room_id: str,
        user_id: str,
        username: str,
        message_data: MessageCreate,
        db: Session
    ) -> MessageResponse:
        new_message = Message(
            room_id=room_id,
            user_id=user_id,
            username=username,
            content=message_data.content
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        return MessageResponse(
            id=new_message.id,
            username=new_message.username,
            content=new_message.content,
            timestamp=new_message.created_at.isoformat()
        )

    @staticmethod
    def get_room_messages(room_id: str, db: Session, limit: int = 50) -> List[MessageResponse]:
        messages = db.exec(
            select(Message)
            .where(Message.room_id == room_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        ).all()

        return [
            MessageResponse(
                id=msg.id,
                username=msg.username,
                content=msg.content,
                timestamp=msg.created_at.isoformat()
            )
            for msg in reversed(messages)
        ]

from sqlmodel import Session, select
from typing import List

from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse


class MessageService:

    @staticmethod
    def create_message(room_id: str, username: str, message_data: MessageCreate, db: Session):
        msg = Message(
            room_id=room_id,
            username=username,
            content=message_data.content
        )

        db.add(msg)
        db.commit()
        db.refresh(msg)

        return MessageResponse(
            id=msg.id,
            username=msg.username,
            content=msg.content,
            timestamp=msg.created_at.strftime("%I:%M %p")
        )

    @staticmethod
    def get_room_messages(room_id: str, db: Session) -> List[MessageResponse]:
        messages = db.exec(
            select(Message)
            .where(Message.room_id == room_id)
            .order_by(Message.created_at)
        ).all()

        return [
            MessageResponse(
                id=m.id,
                username=m.username,
                content=m.content,
                timestamp=m.created_at.strftime("%I:%M %p")
            )
            for m in messages
        ]

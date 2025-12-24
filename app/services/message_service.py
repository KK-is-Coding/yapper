from datetime import datetime, timezone
from sqlmodel import Session, select
from app.database import engine
from app.models import Message

def save_message(room_id, user_id, msg_type, content):
    msg = Message(
        room_id=room_id,
        user_id=user_id,
        type=msg_type,
        content=content,
        created_at=datetime.now(timezone.utc)
    )
    with Session(engine) as session:
        session.add(msg)
        session.commit()
        session.refresh(msg)
    return msg

def load_recent_messages(room_id, limit=30):
    with Session(engine) as session:
        return session.exec(
            select(Message)
            .where(Message.room_id == room_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        ).all()

from datetime import datetime, timezone
from sqlmodel import Session, select

from app.database import engine
from app.models import ChatRoom
from app.utils.time import ensure_utc


def cleanup_rooms():
    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        rooms = session.exec(select(ChatRoom)).all()
        for room in rooms:
            if ensure_utc(room.expires_at) <= now:
                room.is_active = False
        session.commit()

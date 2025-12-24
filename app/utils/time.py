from datetime import datetime, timezone

def ensure_utc(dt: datetime) -> datetime:
    """
    Ensure datetime is timezone-aware (UTC).
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

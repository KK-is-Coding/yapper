from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./yapper.db"

    ALLOWED_ORIGINS: str = "[]"

    MAX_DISTANCE_KM: float = 5.0

    ROOM_EXPIRY_HOURS: int = 2

    def cors_origins(self) -> List[str]:
        try:
            return json.loads(self.ALLOWED_ORIGINS)
        except Exception:
            return []

    class Config:
        env_file = ".env"


settings = Settings()

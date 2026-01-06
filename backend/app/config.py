from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./yapper.db"

    # CORS (parse safely from .env)
    ALLOWED_ORIGINS: str = "[]"

    # Geo
    MAX_DISTANCE_KM: float = 5.0

    # Room
    ROOM_EXPIRY_HOURS: int = 2

    def cors_origins(self) -> List[str]:
        try:
            return json.loads(self.ALLOWED_ORIGINS)
        except Exception:
            return []

    class Config:
        env_file = ".env"


settings = Settings()

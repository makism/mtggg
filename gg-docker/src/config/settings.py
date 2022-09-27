from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class Environment(Enum):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    APP_NAME: str = "MTG Good Game!"
    VERSION: str = "1.0"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

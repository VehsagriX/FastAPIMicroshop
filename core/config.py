from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/shop.db.sqlite3"
    echo: bool = True  # только во время отладки True, а после обязательно False


settings = Settings()

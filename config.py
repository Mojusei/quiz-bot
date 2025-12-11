# config.py
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, computed_field


# Определяем корень проекта как директорию, где лежит config.py
PROJECT_ROOT = Path(__file__).parent.resolve()


class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")

    # Вычисляемый путь к БД по умолчанию (если не задан в .env)
    @computed_field
    @property
    def database_path(self) -> Path:
        return PROJECT_ROOT / "quiz_bot.db"

    @computed_field
    @property
    def database_url(self) -> str:
        # Формат для async SQLAlchemy + aiosqlite
        return f"sqlite+aiosqlite:///{self.database_path.as_posix()}"

    class Config:
        env_file = PROJECT_ROOT / ".env"
        env_file_encoding = "utf-8"


settings = Settings()

from pathlib import Path

from pydantic_settings import BaseSettings

from app.paths import FRONTEND_DIR

DATA_DIR = Path.home() / ".mini_shop"


class Settings(BaseSettings):
    app_name: str = "Mini Shop"
    secret_key: str = "dev-secret-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = f"sqlite:///{DATA_DIR / 'shop.db'}"
    upload_dir: str = str(DATA_DIR / "uploads")


settings = Settings()


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

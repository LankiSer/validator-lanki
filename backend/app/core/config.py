from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Mini Shop"
    secret_key: str = "dev-secret-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./shop.db"
    upload_dir: str = "uploads"


settings = Settings()

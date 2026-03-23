"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings - set these in .env file."""

    # Database - set in .env (PostgreSQL or sqlite:///./inventory.db for dev)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/inventory_saas"

    # JWT
    SECRET_KEY: str = "change-this-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# app/config.py
"""Application configuration from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings loaded from environment (e.g. .env)."""

    # Server
    port: int = 5000
    frontend_url: str = "http://localhost:5173"

    # Auth
    jwt_secret: str = "super-secure-jwt-secret-key-for-development-only"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 10

    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "edutube"

    # Optional: YouTube (YT_KEY) and Gemini (GEMINI_API_KEY)
    yt_key: str = ""
    gemini_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def cors_origins(self) -> list[str]:
        if "," in self.frontend_url:
            return [o.strip() for o in self.frontend_url.split(",")]
        return [self.frontend_url] if self.frontend_url else []


settings = Settings()

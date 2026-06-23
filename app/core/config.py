import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    LOCALHOST: str = os.getenv("LOCALHOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    WEBHOST: str = os.getenv("WEBHOST", "")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "")

    REDIS_CLIENT_URL: str = os.getenv("REDIS_CLIENT_URL", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DECODE_RESPONSES: bool = os.getenv("REDIS_DECODE_RESPONSES", "True").lower() == "true"

    # Auth
    API_KEY: str = os.getenv("API_KEY", "")
    CSRF_SECRET: str = os.getenv("CSRF_SECRET", os.urandom(32).hex())

    # Email (SMTP)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").lower() == "true"
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "")

    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))


settings = Settings()

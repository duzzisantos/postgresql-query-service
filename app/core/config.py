import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    LOCALHOST: str = os.getenv("LOCALHOST", "")
    PORT: int = int(os.getenv("PORT", "8000"))
    WEBHOST: str = os.getenv("WEBHOST", "")

    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")

    @property
    def cors_origins(self) -> list[str]:
        origins = []
        for val in [self.LOCALHOST, self.WEBHOST, *self.ALLOWED_ORIGINS.split(",")]:
            val = val.strip()
            if not val:
                continue
            val = val.rstrip("/")
            if not val.startswith("http"):
                val = f"https://{val}"
            origins.append(val)
        return origins

    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "")

    REDIS_CLIENT_URL: str = os.getenv("REDIS_CLIENT_URL", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DECODE_RESPONSES: bool = (
        os.getenv("REDIS_DECODE_RESPONSES", "True").lower() == "true"
    )

    # Auth
    API_KEY: str = os.getenv("API_KEY", "")
    UNLOCK_KEY: str = os.getenv("UNLOCK_KEY", "")

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

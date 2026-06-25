import hmac
from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
unlock_key_header = APIKeyHeader(name="X-Unlock-Key", auto_error=False)


async def require_api_key(api_key: str = Depends(api_key_header)):
    if not settings.API_KEY:
        return
    if not api_key or not hmac.compare_digest(api_key, settings.API_KEY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")


async def require_unlock_key(unlock_key: str = Depends(unlock_key_header)):
    if not settings.UNLOCK_KEY:
        return
    if not unlock_key or not hmac.compare_digest(unlock_key, settings.UNLOCK_KEY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing unlock key")

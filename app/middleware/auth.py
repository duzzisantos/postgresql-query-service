import hashlib
import hmac
import secrets
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str = Depends(api_key_header)):
    """Reject requests without a valid API key."""
    if not settings.API_KEY:
        # No key configured — auth is disabled (dev mode)
        return
    if not api_key or not hmac.compare_digest(api_key, settings.API_KEY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")


# ── CSRF ──────────────────────────────────────────────────────────

def generate_csrf_token() -> str:
    return secrets.token_hex(32)


def verify_csrf_token(request_token: str, session_token: str) -> bool:
    if not request_token or not session_token:
        return False
    return hmac.compare_digest(request_token, session_token)

import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Per-IP sliding window rate limiter."""

    def __init__(self, app):
        super().__init__(app)
        self._buckets: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        cutoff = now - 60

        bucket = self._buckets[client_ip]
        self._buckets[client_ip] = [t for t in bucket if t > cutoff]

        if len(self._buckets[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded. Try again shortly.")

        self._buckets[client_ip].append(now)
        response = await call_next(request)
        return response

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.middleware.auth import generate_csrf_token, verify_csrf_token

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
CSRF_HEADER = "X-CSRF-Token"
CSRF_COOKIE = "csrf_token"


class CSRFMiddleware(BaseHTTPMiddleware):
    """
    Double-submit cookie pattern:
    - GET requests receive a csrf_token cookie.
    - Mutating requests must echo that token back in the X-CSRF-Token header.
    """

    async def dispatch(self, request: Request, call_next):
        if request.method in SAFE_METHODS:
            response: Response = await call_next(request)
            if CSRF_COOKIE not in request.cookies:
                token = generate_csrf_token()
                response.set_cookie(CSRF_COOKIE, token, httponly=False, samesite="strict", secure=False)
            return response

        cookie_token = request.cookies.get(CSRF_COOKIE, "")
        header_token = request.headers.get(CSRF_HEADER, "")

        if not verify_csrf_token(header_token, cookie_token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token missing or invalid")

        return await call_next(request)

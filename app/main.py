from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.request_context import set_request_context
from app.routes.observability import ensure_observability_table
from app.routes.joiners import joiner_router
from app.routes.mutators import mutator_router
from app.routes.select_all import select_all_router
from app.routes.select_by_columns import select_by_column_router
from app.routes.tables import table_router
from app.routes.connection_verify import connection_verify
from app.download_queries.queried_downloads import queried_download_router
from app.routes.observability import log_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        ensure_observability_table()
    except Exception:
        pass
    yield


app = FastAPI(title="PostgreSQL Query Service", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key", "X-Unlock-Key"],
)
app.add_middleware(RateLimiterMiddleware)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        source_ip = request.client.host if request.client else ""
        endpoint = request.url.path
        dest_ip = settings.LOCALHOST
        set_request_context(source_ip, endpoint, dest_ip)
        return await call_next(request)


app.add_middleware(RequestContextMiddleware)


@app.get("/")
async def root():
    return {"message": "enter /docs to view API documentation"}


app.include_router(log_router)
app.include_router(connection_verify)
app.include_router(joiner_router)
app.include_router(mutator_router)
app.include_router(select_all_router)
app.include_router(select_by_column_router)
app.include_router(table_router)
app.include_router(queried_download_router)

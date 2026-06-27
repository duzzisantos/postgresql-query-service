from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.request_context import set_request_context
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
    yield


app = FastAPI(title="PostgreSQL Query Service", version="2.0.0", lifespan=lifespan)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        source_ip = request.client.host if request.client else ""
        endpoint = request.url.path
        dest_ip = settings.WEBHOST
        set_request_context(source_ip, endpoint, dest_ip)
        return await call_next(request)


app.add_middleware(RequestContextMiddleware)
app.add_middleware(RateLimiterMiddleware)
_origins = settings.cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost:5173",
        settings.WEBHOST,
        settings.POSTGRES_URL,
        settings.CELERY_BROKER_URL,
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "enter /docs to view API documentation"}


##Routes


app.include_router(log_router)
app.include_router(connection_verify)
app.include_router(joiner_router)
app.include_router(mutator_router)
app.include_router(select_all_router)
app.include_router(select_by_column_router)
app.include_router(table_router)
app.include_router(queried_download_router)

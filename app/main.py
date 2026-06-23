from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.csrf import CSRFMiddleware
from app.routes.joiners import joiner_router
from app.routes.mutators import mutator_router
from app.routes.select_all import select_all_router
from app.routes.select_by_columns import select_by_column_router
from app.routes.tables import table_router
from app.routes.connection_verify import connection_verify
from app.download_queries.queried_downloads import queried_download_router
from app.routes.observability import log_router
import uvicorn

app = FastAPI(title="Database Query Interface", version="2.0.0")

origins = [o for o in [settings.LOCALHOST, settings.WEBHOST] if o]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key", "X-CSRF-Token"],
)
app.add_middleware(RateLimiterMiddleware)
app.add_middleware(CSRFMiddleware)


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


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.LOCALHOST, port=settings.PORT, reload=True)

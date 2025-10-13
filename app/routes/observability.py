from loguru import logger
from fastapi import APIRouter, status
import sys
## Observe activities going on in server: for example queries, connection verifications, validation errors, responses etc

log_router = APIRouter()

@log_router.post("/GetLog", status_code=status.HTTP_200_OK)
async def getQueryLog(log_type: str, message: str | dict | list[str]):

    if log_type == "error":
        logger.add(sys.stderr, format="{level} : {time} : {message}: {process}")
        logger.error(message)

    elif log_type.__eq__("success") or log_type.__eq__("dml"):
        logger.add(sys.stdout, format="{level} : {time} : {message}: {process}")
        logger.success(message)


async def handle_logging(log_type: str, message: str | dict | list[dict]):
    ## store in logging database or observability service
    return await getQueryLog(log_type, message)
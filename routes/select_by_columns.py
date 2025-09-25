from fastapi import APIRouter, status
from models.request_model import RequestModel
from redis_caching import manage_caching
from utils.request import request

select_by_column_router = APIRouter()
CACHE_TIME = int(1200)


@select_by_column_router.post("/GetByColumns", status_code=status.HTTP_200_OK)
async def getByColumns(model: RequestModel):
    comma_separated_columns = ", ".join(model.columns)
    await request("SELECT %s FROM %s", (comma_separated_columns, model.table))
    


@select_by_column_router.post("/GetByColumnsAndOrderBy", status_code=status.HTTP_200_OK)
async def getByColumnsOrderBy(model: RequestModel):
    multi_cols = ", ".join(model.columns)
    await request("SELECT % FROM %s ORDER BY %s", (multi_cols, model.table, model.order))
  


@select_by_column_router.post("/GetByColumnsAndLimit", status_code=status.HTTP_200_OK)
async def getByColumnsAndLimit(model: RequestModel):
    key = "GetByColumnsAndLimit"
    multi_cols = ", ".join(model.columns)
    await request("SELECT %s FROM %s LIMIT %s", (multi_cols, model.table, model.limit))
  
        
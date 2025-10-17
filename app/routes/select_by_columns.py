from fastapi import APIRouter, status
from app.models.request_model import ByColumns, ByColumnsAndLimit, ByColumnsAndOrder
from app.utils.request import request
from app.middleware.no_injection import validate_params_against_sqli
from psycopg2 import sql

select_by_column_router = APIRouter()
CACHE_TIME = int(1200)


@select_by_column_router.post("/GetByColumns", status_code=status.HTTP_200_OK) ##ça marche
async def getByColumns(model: ByColumns):
    await validate_params_against_sqli(dict(model))
    comma_separated_columns = ", ".join(model.columns)
    res = await request(f"SELECT {comma_separated_columns} FROM {model.table}", (comma_separated_columns, model.table))
    return res
    

@select_by_column_router.post("/GetByColumnsAndOrderBy", status_code=status.HTTP_200_OK) ##ça marche
async def getByColumnsOrderBy(model: ByColumnsAndOrder):
    await validate_params_against_sqli(dict(model))
    multi_cols = ", ".join(model.columns)
    res = await request(f"SELECT {multi_cols} FROM {model.table} ORDER BY {model.order}", (multi_cols, model.table, model.order))
    return res
  


@select_by_column_router.post("/GetByColumnsAndLimit", status_code=status.HTTP_200_OK) ##ça marche
async def getByColumnsAndLimit(model: ByColumnsAndLimit):
    await validate_params_against_sqli(dict(model))
    multi_cols = ", ".join(model.columns)
    res = await request(f"SELECT {multi_cols} FROM {model.table} LIMIT {model.limit}", (multi_cols, model.table, model.limit))
    return res
  
        
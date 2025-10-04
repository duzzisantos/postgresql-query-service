from fastapi import APIRouter, status, Query
from utils.request import request
from middleware.no_injection import validate_params_against_sqli
from models.request_model import CreateTable

table_router = APIRouter()
CACHE_TIME = int(1200)

@table_router.post("/FindTables") ##ça marche
async def findTables():
    query = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name
    """
    res =  await request(query, None)
    return res
   

@table_router.post("/CreateTable", status_code=status.HTTP_201_CREATED) ##ça marche
async def createTable(model: CreateTable):
    await validate_params_against_sqli(dict(model))
    multi_cols = ", ".join(model.column_names_with_properties)

    res =  await request(f"CREATE TABLE {model.table_name} ({multi_cols})", ())
    return res

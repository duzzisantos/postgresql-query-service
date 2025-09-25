from fastapi import APIRouter, status, Query
from utils.request import request
from redis_caching import manage_caching

table_router = APIRouter()
CACHE_TIME = int(1200)

@table_router.post("/FindTables")
async def findTables():
    await request("SELECT table_schema, table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema') ORDER BY table_schema, table_name", None)
   

@table_router.post("/CreateTable", status_code=status.HTTP_201_CREATED)
async def createTable(columns: list[str], table_name=Query(...)):
    multi_cols = ", ".join(columns)
    print(multi_cols)
    

    await request(f"CREATE TABLE {table_name} ({multi_cols})", None)


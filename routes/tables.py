from fastapi import APIRouter, status, Query
from utils.request import request

table_router = APIRouter()

@table_router.post("/FindTables")
async def findTables():
    request("SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema')", None)


@table_router.post("/CreateTable", status_code=status.HTTP_201_CREATED)
async def createTable(columns: list[str], table_name=Query(...)):
    multi_cols = ", ".join(columns)
    print(multi_cols)
    

    request(f"CREATE TABLE {table_name} ({multi_cols})", None)


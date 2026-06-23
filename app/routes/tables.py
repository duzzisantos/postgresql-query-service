from fastapi import APIRouter, status, Depends
from psycopg2 import sql
from app.utils.request import request
from app.middleware.no_injection import validate_params_against_sqli, validate_identifier
from app.middleware.auth import require_api_key
from app.models.request_model import CreateTable

table_router = APIRouter(dependencies=[Depends(require_api_key)])


@table_router.post("/FindTables")
async def findTables():
    # Static query — no user input
    query = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name
    """
    return await request(query)


@table_router.post("/CreateTable", status_code=status.HTTP_201_CREATED)
async def createTable(model: CreateTable):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table_name, "table name")

    # Column definitions are structural DDL — validate each starts with a safe identifier
    for col_def in model.column_names_with_properties:
        col_name = col_def.strip().split()[0]
        validate_identifier(col_name, "column name")

    col_defs = sql.SQL(", ").join(sql.SQL(c) for c in model.column_names_with_properties)
    query = sql.SQL("CREATE TABLE {} ({})").format(sql.Identifier(model.table_name), col_defs)
    return await request(query)

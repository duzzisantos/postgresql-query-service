from fastapi import APIRouter, status, Depends
from psycopg2 import sql
from app.models.request_model import ByColumns, ByColumnsAndLimit, ByColumnsAndOrder
from app.middleware.no_injection import validate_params_against_sqli, validate_identifier, validate_identifier_list
from app.middleware.auth import require_api_key
from app.utils.request import request

select_by_column_router = APIRouter(dependencies=[Depends(require_api_key)])


@select_by_column_router.post("/GetByColumns", status_code=status.HTTP_200_OK)
async def getByColumns(model: ByColumns):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier_list(model.columns)
    cols = sql.SQL(", ").join(sql.Identifier(c) for c in model.columns)
    query = sql.SQL("SELECT {} FROM {}").format(cols, sql.Identifier(model.table))
    return await request(query)


@select_by_column_router.post("/GetByColumnsAndOrderBy", status_code=status.HTTP_200_OK)
async def getByColumnsOrderBy(model: ByColumnsAndOrder):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier_list(model.columns)
    validate_identifier(model.order, "order column")
    cols = sql.SQL(", ").join(sql.Identifier(c) for c in model.columns)
    query = sql.SQL("SELECT {} FROM {} ORDER BY {}").format(
        cols, sql.Identifier(model.table), sql.Identifier(model.order),
    )
    return await request(query)


@select_by_column_router.post("/GetByColumnsAndLimit", status_code=status.HTTP_200_OK)
async def getByColumnsAndLimit(model: ByColumnsAndLimit):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier_list(model.columns)
    cols = sql.SQL(", ").join(sql.Identifier(c) for c in model.columns)
    query = sql.SQL("SELECT {} FROM {} LIMIT %s").format(cols, sql.Identifier(model.table))
    return await request(query, (model.limit,))

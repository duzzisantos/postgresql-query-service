from fastapi import APIRouter, Depends
from typing import Literal
from psycopg2 import sql
from app.models.request_model import TableJoinModel, SubQueryExists
from app.middleware.no_injection import validate_params_against_sqli, validate_identifier, validate_identifier_list
from app.middleware.auth import require_api_key
from app.utils.request import request

joiner_router = APIRouter(dependencies=[Depends(require_api_key)])


@joiner_router.post("/GetTableJoin")
async def getTableJoin(model: TableJoinModel, join_type: Literal["FULL", "RIGHT", "LEFT", "INNER"]):
    await validate_params_against_sqli(dict(model))
    validate_identifier_list(model.columns)
    validate_identifier(model.primary_table, "primary table")
    validate_identifier(model.secondary_table, "secondary table")
    validate_identifier(model.common_key, "common key")

    cols = sql.SQL(", ").join(sql.Identifier(c) for c in model.columns)
    # join_type is constrained to the Literal — safe to interpolate
    query = sql.SQL("SELECT {} FROM {} " + join_type + " JOIN {} ON {}.{} = {}.{}").format(
        cols,
        sql.Identifier(model.primary_table),
        sql.Identifier(model.secondary_table),
        sql.Identifier(model.primary_table), sql.Identifier(model.common_key),
        sql.Identifier(model.secondary_table), sql.Identifier(model.common_key),
    )
    return await request(query)


@joiner_router.post("/SubQueryExists")
async def getExists(model: SubQueryExists, operator: Literal["NOT EXISTS", "EXISTS"]):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.primary_column, "primary column")
    validate_identifier(model.primary_table, "primary table")
    validate_identifier(model.sub_query_select, "sub query select")
    validate_identifier(model.sub_query_table, "sub query table")
    validate_identifier(model.sub_query_where_column, "sub query where column")

    # operator is constrained to Literal — safe
    query = sql.SQL(
        "SELECT {} FROM {} WHERE " + operator + " (SELECT {} FROM {} WHERE {} = %s)"
    ).format(
        sql.Identifier(model.primary_column),
        sql.Identifier(model.primary_table),
        sql.Identifier(model.sub_query_select),
        sql.Identifier(model.sub_query_table),
        sql.Identifier(model.sub_query_where_column),
    )
    return await request(query, (model.sub_query_where_value,))

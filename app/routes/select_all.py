import re
from fastapi import APIRouter, status, HTTPException, Depends
from psycopg2 import sql
from app.models.request_model import (
    GetAll, OrderBy, LimitAndOffset, WithLimit, AllWhere, AllBetween,
    AllGroupByModel, AllWhereIn, AllWhereAverageModel, AllWhereAndCount,
    AllWhereMatches, AllWhereOrderBy,
)
from app.middleware.no_injection import validate_params_against_sqli, validate_identifier
from app.middleware.auth import require_api_key
from app.utils.request import request
from app.redis_caching.manage_caching import manage_caching

select_all_router = APIRouter(dependencies=[Depends(require_api_key)])
CACHE_TTL = 1200


@select_all_router.post("/GetAll", status_code=status.HTTP_200_OK)
async def getAll(model: GetAll):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(model.table))
    return await manage_caching(f"getall:{model.table}", CACHE_TTL, lambda: request(query))


@select_all_router.post("/GetAllOrderBy", status_code=status.HTTP_200_OK)
async def getAllOrderBy(model: OrderBy):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.order, "order column")
    query = sql.SQL("SELECT * FROM {} ORDER BY {}").format(
        sql.Identifier(model.table), sql.Identifier(model.order),
    )
    return await request(query)


@select_all_router.post("/GetAllWithLimitAndOffset", status_code=status.HTTP_200_OK)
async def getAllWithLimitAndOffset(model: LimitAndOffset):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    query = sql.SQL("SELECT * FROM {} LIMIT %s OFFSET %s").format(sql.Identifier(model.table))
    return await request(query, (model.limit, model.offset))


@select_all_router.post("/GetAllWithLimit", status_code=status.HTTP_200_OK)
async def getAllWithLimit(model: WithLimit):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    query = sql.SQL("SELECT * FROM {} LIMIT %s").format(sql.Identifier(model.table))
    return await request(query, (model.limit,))


@select_all_router.post("/GetAllWhere", status_code=status.HTTP_200_OK)
async def getAllWhere(model: AllWhere):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    query, params = _build_where_query(model.table, model.conditions)
    return await request(query, params)


@select_all_router.post("/GetAllWhereAndOrderBy", status_code=status.HTTP_200_OK)
async def getAllWhereAndOrderBy(model: AllWhereOrderBy):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.order, "order column")
    query, params = _build_where_query(model.table, model.conditions, order_by=model.order)
    return await request(query, params)


@select_all_router.post("/GetAllBetween", status_code=status.HTTP_200_OK)
async def getAllBetween(model: AllBetween):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.column, "column")
    query = sql.SQL("SELECT * FROM {} WHERE {} BETWEEN %s AND %s").format(
        sql.Identifier(model.table), sql.Identifier(model.column),
    )
    return await request(query, (str(model.start), str(model.end)))


@select_all_router.post("/GetAllWhereMatches", status_code=status.HTTP_200_OK)
async def getAllWhereMatches(model: AllWhereMatches):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.column, "column")
    query = sql.SQL("SELECT * FROM {} WHERE {} LIKE %s").format(
        sql.Identifier(model.table), sql.Identifier(model.column),
    )
    return await request(query, (str(model.wild_card),))


@select_all_router.post("/GetAllWhereIn", status_code=status.HTTP_200_OK)
async def getAllWhereIn(model: AllWhereIn):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.column, "column")
    items = model.search_parameters if isinstance(model.search_parameters, list) else [model.search_parameters]
    placeholders = sql.SQL(", ").join([sql.Placeholder()] * len(items))
    query = sql.SQL("SELECT * FROM {} WHERE {} IN ({})").format(
        sql.Identifier(model.table), sql.Identifier(model.column), placeholders,
    )
    return await request(query, tuple(str(i) for i in items))


@select_all_router.post("/GetAllWhereAndCount", status_code=status.HTTP_200_OK)
async def getAllWhereAndCount(model: AllWhereAndCount):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.primary_column, "primary column")
    validate_identifier(model.secondary_column, "secondary column")
    query = sql.SQL("SELECT COUNT({}) FROM {} WHERE {} = %s").format(
        sql.Identifier(model.primary_column), sql.Identifier(model.table), sql.Identifier(model.secondary_column),
    )
    return await request(query, (model.search_parameter,))


@select_all_router.post("/GetAllWhereAverage", status_code=status.HTTP_200_OK)
async def getAllWhereAndAverage(model: AllWhereAverageModel):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.column, "column")
    query = sql.SQL("SELECT AVG({})::NUMERIC(10,2) FROM {}").format(
        sql.Identifier(model.column), sql.Identifier(model.table),
    )
    return await request(query)


@select_all_router.post("/GetAllGroupBy", status_code=status.HTTP_200_OK)
async def getAllWhereAndGroupBy(model: AllGroupByModel):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.primary_column, "primary column")
    validate_identifier(model.secondary_column, "secondary column")
    query = sql.SQL("SELECT {}, COUNT({}) FROM {} GROUP BY {}").format(
        sql.Identifier(model.secondary_column), sql.Identifier(model.primary_column),
        sql.Identifier(model.table), sql.Identifier(model.secondary_column),
    )
    return await request(query)


# ── WHERE clause builder ──────────────────────────────────────────

_COND_PATTERN = re.compile(r"^(\w+)\s*(=|!=|<>|>=|<=|>|<)\s*(.+)$")


def _build_where_query(table: str, conditions: list[str], order_by: str = None):
    """Parse 'column op value' strings into parameterized SQL."""
    parts = []
    params = []

    for cond in conditions:
        m = _COND_PATTERN.match(cond.strip())
        if not m:
            raise HTTPException(status_code=422, detail=f"Invalid condition: '{cond}'. Expected 'column operator value'.")
        col, op, val = m.group(1), m.group(2), m.group(3).strip().strip("'\"")
        validate_identifier(col, "condition column")
        # Operator is matched by regex — only =, !=, <>, >, <, >=, <= are possible
        parts.append(sql.SQL("{} " + op + " %s").format(sql.Identifier(col)))
        params.append(val)

    where_clause = sql.SQL(" AND ").join(parts)

    if order_by:
        query = sql.SQL("SELECT * FROM {} WHERE {} ORDER BY {}").format(
            sql.Identifier(table), where_clause, sql.Identifier(order_by),
        )
    else:
        query = sql.SQL("SELECT * FROM {} WHERE {}").format(sql.Identifier(table), where_clause)

    return query, tuple(params)

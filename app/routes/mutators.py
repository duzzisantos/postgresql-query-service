from fastapi import APIRouter, status, Depends
from psycopg2 import sql
from app.models.request_model import CreateRow, CreateMany, DeleteRow, DeleteMany, UpdateMany, UpdateRow
from app.middleware.no_injection import validate_params_against_sqli, validate_identifier, validate_identifier_list
from app.middleware.auth import require_api_key
from app.utils.request import request
from app.utils.utilities import build_set_clause
from app.redis_caching.manage_caching import invalidate_cache

mutator_router = APIRouter(dependencies=[Depends(require_api_key)])


@mutator_router.post("/CreateOne")
async def createOne(model: CreateRow):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier_list(model.columns)

    cols = sql.SQL(", ").join(sql.Identifier(c) for c in model.columns)
    placeholders = sql.SQL(", ").join([sql.Placeholder()] * len(model.values))
    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(model.table), cols, placeholders,
    )
    result = await request(query, tuple(model.values))
    await invalidate_cache(f"getall:{model.table}*")
    return result


@mutator_router.post("/CreateMany")
async def createMany(model: CreateMany):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier_list(model.columns)

    cols = sql.SQL(", ").join(sql.Identifier(c) for c in model.columns)
    single_row = sql.SQL("({})").format(sql.SQL(", ").join([sql.Placeholder()] * len(model.columns)))
    all_rows = sql.SQL(", ").join([single_row] * len(model.values))

    query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
        sql.Identifier(model.table), cols, all_rows,
    )
    # Flatten the nested list into a single params tuple
    flat_params = tuple(v for row in model.values for v in row)
    result = await request(query, flat_params)
    await invalidate_cache(f"getall:{model.table}*")
    return result


@mutator_router.post("/DeleteById")
async def deleteById(model: DeleteRow):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.primary_column, "primary column")

    query = sql.SQL("DELETE FROM {} WHERE {} = %s").format(
        sql.Identifier(model.table), sql.Identifier(model.primary_column),
    )
    result = await request(query, (model.id,))
    await invalidate_cache(f"getall:{model.table}*")
    return result


@mutator_router.post("/DeleteMany")
async def deleteMany(model: DeleteMany):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.primary_column, "primary column")

    # Delete by list of IDs, not the entire table
    placeholders = sql.SQL(", ").join([sql.Placeholder()] * len(model.primary_key))
    query = sql.SQL("DELETE FROM {} WHERE {} IN ({})").format(
        sql.Identifier(model.table), sql.Identifier(model.primary_column), placeholders,
    )
    result = await request(query, tuple(model.primary_key))
    await invalidate_cache(f"getall:{model.table}*")
    return result


@mutator_router.post("/UpdateOne")
async def updateOne(model: UpdateRow):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.primary_column, "primary column")
    validate_identifier(model.secondary_column, "set column")

    query = sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s").format(
        sql.Identifier(model.table), sql.Identifier(model.secondary_column), sql.Identifier(model.primary_column),
    )
    result = await request(query, (model.set_value, model.where_value))
    await invalidate_cache(f"getall:{model.table}*")
    return result


@mutator_router.post("/UpdateMany", status_code=status.HTTP_200_OK)
async def updateMany(model: UpdateMany):
    await validate_params_against_sqli(dict(model))
    validate_identifier(model.table, "table")
    validate_identifier(model.where_column, "where column")
    validate_identifier_list(model.set_columns)

    set_clause, set_params = build_set_clause(model.set_columns, model.set_values)
    if set_clause is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="set_columns and set_values must have equal length")

    query = sql.SQL("UPDATE {} SET {} WHERE {} = %s").format(
        sql.Identifier(model.table), set_clause, sql.Identifier(model.where_column),
    )
    params = set_params + (model.where_value,)
    result = await request(query, params)
    await invalidate_cache(f"getall:{model.table}*")
    return result

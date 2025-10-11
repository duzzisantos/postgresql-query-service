from fastapi import APIRouter
from typing import Literal
from models.request_model import TableJoinModel, SubQueryExists
from middleware.connection_state import get_connection
from utils.request import request
from middleware.no_injection import validate_params_against_sqli

joiner_router = APIRouter()

cursor = get_connection().cursor()

@joiner_router.post("/GetTableJoin")
async def getTableJoin(model: TableJoinModel, join_type: Literal["FULL", "RIGHT", "LEFT", "INNER"]): # full, inner, right, and left joins
    await validate_params_against_sqli(dict(model))
    multi_cols = ", ".join(model.columns)
    result = await request(f"SELECT {multi_cols} FROM {model.primary_table} {join_type} JOIN {model.secondary_table} ON {model.primary_table[model.common_key]}  = {model.secondary_table[model.common_key]}", 
                                ())
    return result
    
    
@joiner_router.post("/SubQueryExists")
async def getExists(model: SubQueryExists, operator: Literal['NOT EXISTS', 'EXISTS']):
    await validate_params_against_sqli(dict(model))
    query_template = f"SELECT {model.primary_column} FROM {model.primary_table} WHERE {operator} (SELECT {model.sub_query_select} FROM {model.sub_query_table} WHERE {model.sub_query_where_column} = {model.sub_query_where_value})"
    result = await request(query_template, ())
    return result






from fastapi import APIRouter, Query
from models.request_model import TableJoinModel
from middleware.connection_state import get_connection
from utils.request import request
from middleware.no_injection import validate_params_against_sqli

joiner_router = APIRouter()

cursor = get_connection().cursor()

@joiner_router.post("/GetTableJoin")
async def getTableJoin(model: TableJoinModel): ## Refactor
    await validate_params_against_sqli(dict(model))
    multi_cols = multi_cols = ", ".join(model.columns)
    result = await request("SELECT %s FROM %s %s JOIN %s ON %s  = %s", 
                                (multi_cols, model.primary_table, model.join_type, model.secondary_table, model.primary_table[model.common_key],
                                    model.secondary_table[model.common_key]))
    return result
    
    
    





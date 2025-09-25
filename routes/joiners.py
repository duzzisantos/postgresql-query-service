from fastapi import APIRouter, Query
from models.request_model import RequestModel
from middleware.connection_state import get_connection
from redis_caching.manage_caching import manage_caching
from utils.request import request

joiner_router = APIRouter()

cursor = get_connection().cursor()

@joiner_router.post("/GetTableJoin")
async def getTableJoin(model: RequestModel):
    multi_cols = multi_cols = ", ".join(model.columns)
    await request("SELECT %s FROM %s %s JOIN %s ON %s  = %s", 
                                (multi_cols, model.primary_table, model.join_type, model.secondary_table, model.primary_table[model.common_key],
                                    model.secondary_table[model.common_key]))
    
    
    





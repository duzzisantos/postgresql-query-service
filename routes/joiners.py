from fastapi import APIRouter, HTTPException, status
from middleware.errorlogger import errorLogger
from middleware.success_logger import successLogger
from query_builders.join_builders.basic_joins import BasicJoin
from models.request_model import RequestModel
from routes.connection_verify import client_configs

joiner_router = APIRouter()
cursor = client_configs



@joiner_router.post("/GetTableJoiner")
async def getLeftJoin(request_body: RequestModel):
    errorLogger(request_body.columns)
    errorLogger(request_body.join_type)
    errorLogger(request_body.primary_table)
    errorLogger(request_body.secondary_table)
    errorLogger(request_body.common_key)
    
    query = BasicJoin(request_body.columns, request_body.join_type, 
                      request_body.primary_table, request_body.secondary_table,
                        request_body.common_key, cursor)

    if(request_body.join_type.__eq__('left_join')):
        return query.leftJoin()
    elif(request_body.join_type.__eq__('right_join')):
        return query.rightJoin()
    elif(request_body.join_type.__eq__('inner_join')):
        return query.innerJoin()
    else:
        return query.fullJoin()
    





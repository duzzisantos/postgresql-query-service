from fastapi import APIRouter, HTTPException, status
from middleware.errorlogger import errorLogger
from middleware.log_error import log_error
from middleware.success_logger import successLogger
from query_builders.join_builders.basic_joins import BasicJoin
from models.request_model import RequestModel
from routes.connection_verify import connection_verify

joiner_router = APIRouter()

cursor = connection_verify

@joiner_router.post("/GetTableJoiner")
async def getLeftJoin(request_body: RequestModel):
    
    body = [request_body.columns, request_body.join_type, request_body.primary_table,
             request_body.secondary_table, request_body.common_key]
    log_error(body)
    
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
    





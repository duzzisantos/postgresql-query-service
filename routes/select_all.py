from fastapi import APIRouter, status
from middleware.errorlogger import errorLogger
from middleware.success_logger import successLogger
from middleware.log_error import log_error
from services.queries.selectors.select_all import SelectAll
from models.request_model import RequestModel
from routes.connection_verify import connection_verify


select_all_router = APIRouter()
operations = SelectAll()
cursor = connection_verify

@select_all_router.post("/GetAll", status_code=status.HTTP_200_OK)
async def getAll(table: str):
    errorLogger([table])
    successLogger(cursor=cursor, operations=operations.getAll(table))

@select_all_router.post("/GetAllOrderBy", status_code=status.HTTP_200_OK)
async def getAllOrderBy(model: RequestModel):
    log_error([model.table, model.order])

    return operations.getAllOrderBy(model.table, model.order, cursor)
    
@select_all_router.post("/GetAllWithLimitAndOffset", status_code=status.HTTP_200_OK)
async def getAllWithLimitAndOffset(model: RequestModel):
    log_error([model.table, model.limit, model.offset])

    return operations.getAllWithLimitAndOffset(model.table, model.limit, model.offset, cursor)
    

@select_all_router.post("/GetAllWithLimit", status_code=status.HTTP_200_OK)
async def getAllWithLimit(model: RequestModel):
    log_error([model.table, model.limit])

    return operations.getAllWithLimit(model.table, model.limit, cursor)
    
   
@select_all_router.post("/GetAllWhere", status_code=status.HTTP_200_OK)
def getAllWhere(model: RequestModel):
    log_error([model.table, model.conditions])

    return operations.getAllWhere(model.table, model.conditions, cursor)

@select_all_router.post("/GetAllWhereAndOrderBy", status_code=status.HTTP_200_OK)
async def getAllWhereAndOrderBy(model: RequestModel):
    log_error([model.table, model.conditions, model.order])

    return operations.getAllWhereAndOrderBy(model.table, model.conditions, model.order, cursor)

@select_all_router.post("/GetAllBetween", status_code=status.HTTP_200_OK)
async def getAllBetween(model: RequestModel):
    log_error([model.table, model.query_range])

    return operations.getAllBetween(model.table, model.query_range, cursor)


@select_all_router.post("/GetAllWhereMatches", status_code=status.HTTP_200_OK)
async def getAllWhereMatches(model: RequestModel):
    log_error([model.table, model.columns, model.wild_cards])

    return operations.getAllWhereMatches(model.table, model.columns, model.wild_cards, cursor)


@select_all_router.post("/GetAllWhereIn", status_code=status.HTTP_200_OK)
async def getAllWhereIn(model: RequestModel):
    log_error([model.table, model.columns, model.search_parameters])

    return operations.getAllWhereIn(model.table, model.columns, model.search_parameters, cursor)

@select_all_router.post("/GetAllWhereAndCount", status_code=status.HTTP_200_OK)
async def getAllWhereAndCount(request: RequestModel):
    log_error([request.table, request.primary_column, 
                                          request.secondary_column, request.search_parameters])

    return operations.getAllWhereAndcount(request.table, request.primary_column, 
                                          request.secondary_column, request.search_parameters, cursor)


@select_all_router.post("/GetAllWhereAverage", status_code=status.HTTP_200_OK)
def getAllWhereAndCount(request: RequestModel):
    log_error([request.table, request.column])

    return operations.getAllWhereAndAverage(request.table, request.column, cursor)


@select_all_router.post("/GetAllGroupBy", status_code=status.HTTP_200_OK)
def getAllWhereAndCount(request: RequestModel):
    log_error([request.table, request.primary_column, request.secondary_column])
    
    return operations.getAllGroupBy(request.table, request.primary_column, request.secondary_column, cursor)







from fastapi import FastAPI, HTTPException, status
from middleware.errorlogger import errorLogger
from middleware.success_logger import successLogger
from services.queries.selectors.select_all import SelectAll
from models.request_model import RequestModel
import psycopg2 # type: ignore

connection = psycopg2.connect(dbname="akuko-uwa", user="postgres", password="dummy", host="localhost", port="5432")
cursor = connection.cursor()

app = FastAPI()
http_response = HTTPException()
operations = SelectAll()

## TODO: Improve error logger to avoid repetition
## TODO: Add selected DB Engine checker middleware one-level above this on API gateway

@app.post("/GetAll", status_code=status.HTTP_200_OK)
async def getAll(table: str):
    errorLogger(table)
    successLogger(cursor=cursor, operations=operations.getAll(table))

@app.post("/GetAllOrderBy", status_code=status.HTTP_200_OK)
async def getAllOrderBy(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.order)

    return operations.getAllOrderBy(model.table, model.order, cursor)
    
@app.post("/GetAllWithLimitAndOffset", status_code=status.HTTP_200_OK)
async def getAllWithLimitAndOffset(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.limit)
    errorLogger(model.offset)

    return operations.getAllWithLimitAndOffset(model.table, model.limit, model.offset)
    

@app.post("/GetAllWithLimit", status_code=status.HTTP_200_OK)
async def getAllWithLimit(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.limit)

    return operations.getAllWithLimit(model.table, model.limit, cursor)
    
   
@app.post("/GetAllWhere", status_code=status.HTTP_200_OK)
def getAllWhere(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.conditions)

    return operations.getAllWhere(model.table, model.conditions, cursor)

@app.post("/GetAllWhereAndOrderBy", status_code=status.HTTP_200_OK)
async def getAllWhereAndOrderBy(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.conditions)
    errorLogger(model.order)

    return operations.getAllWhereAndOrderBy(model.table, model.conditions, model.order, cursor)

@app.post("/GetAllBetween", status_code=status.HTTP_200_OK)
async def getAllBetween(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.query_range)

    return operations.getAllBetween(model.table, model.query_range, cursor)


@app.post("/GetAllWhereMatches", status_code=status.HTTP_200_OK)
async def getAllWhereMatches(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.columns)
    errorLogger(model.wild_cards)

    return operations.getAllWhereMatches(model.table, model.columns, model.wild_cards, cursor)


@app.post("/GetAllWhereIn", status_code=status.HTTP_200_OK)
async def getAllWhereIn(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.columns)
    errorLogger(model.search_parameters)

    return operations.getAllWhereIn(model.table, model.columns, model.search_parameters, cursor)

@app.post("/GetAllWhereAndCount", status_code=status.HTTP_200_OK)
async def getAllWhereAndCount(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.primary_column)
    errorLogger(request.secondary_column)
    errorLogger(request.search_parameters)

    return operations.getAllWhereAndcount(request.table, request.primary_column, 
                                          request.secondary_column, request.search_parameters, cursor)


@app.post("/GetAllWhereAverage", status_code=status.HTTP_200_OK)
def getAllWhereAndCount(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.column)

    return operations.getAllWhereAndAverage(request.table, request.column, cursor)


@app.post("/GetAllGroupBy", status_code=status.HTTP_200_OK)
def getAllWhereAndCount(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.primary_column)
    errorLogger(request.secondary_column)
    
    return operations.getAllGroupBy(request.table, request.primary_column, request.secondary_column, cursor)







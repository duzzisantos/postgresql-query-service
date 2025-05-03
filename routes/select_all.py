from fastapi import FastAPI, HTTPException, status
from middleware.errorlogger import errorLogger
from middleware.success_logger import successLogger
from services.queries.selectors.select_all import SelectAll
import psycopg2 # type: ignore

connection = psycopg2.connect(dbname="akuko-uwa", user="postgres", password="dummy", host="localhost", port="5432")
cursor = connection.cursor()

app = FastAPI()
http_response = HTTPException()
operations = SelectAll()

## TODO: Improve error logger to avoid repetition
## TODO: Add selected DB Engine checker middleware one-level above this on API gateway

@app.post("/GetAll/{table}", status_code=status.HTTP_200_OK)
def getAll(table: str):
    errorLogger(table)
    successLogger(cursor=cursor, operations=operations.getAll(table))

@app.post("/GetAllOrderBy/{table}/{order}", status_code=status.HTTP_200_OK)
def getAllOrderBy(table: str, order: str):
    errorLogger(table)
    errorLogger(order)

    successLogger(cursor=cursor, operations=operations.getAllOrderBy(table, order))
    
@app.post("/GetAllWithLimitAndOffset/{table}/{limit}/{offset}", status_code=status.HTTP_200_OK)
def getAllWithLimitAndOffset(table: str, limit: int, offset: int):
    errorLogger(table)
    errorLogger(limit)
    errorLogger(offset)

    successLogger(cursor=cursor, operations=operations.getAllWithLimitAndOffset(table, limit, offset))
    

@app.post("/GetAllWithLimit/{table}/{limit}", status_code=status.HTTP_200_OK)
def getAllWithLimit(table: str, limit: int):
    errorLogger(table)
    errorLogger(limit)

    successLogger(cursor=cursor, operations=operations.getAllWithLimit(table, limit))
    
   
@app.post("/GetAllWhere/{table}/{conditions}", status_code=status.HTTP_200_OK)
def getAllWhere(table, conditions):
    errorLogger(table)
    errorLogger(conditions)

    successLogger(cursor=cursor, operations=operations.getAllWhere(table, conditions))

@app.post("/GetAllWhereAndOrderBy/{table}/{conditions}/{order}", status_code=status.HTTP_200_OK)
def getAllWhereAndOrderBy(table, conditions, order):
    errorLogger(table)
    errorLogger(conditions)
    errorLogger(order)

    successLogger(cursor=cursor, operations=operations.getAllWhereAndOrderBy(table, conditions, order))

@app.post("/GetAllBetween/{table}/{range}", status_code=status.HTTP_200_OK)
def getAllBetween(table, range):
    errorLogger(table)
    errorLogger(range)

    successLogger(cursor, operations=operations.getAllBetween(table, range))


@app.post("/GetAllWhereMatches/{table}/{columns}/{wild_cards}", status_code=status.HTTP_200_OK)
def getAllWhereMatches(table, columns, wild_cards):
    errorLogger(table)
    errorLogger(columns)
    errorLogger(wild_cards)

    successLogger(cursor, operations=operations.getAllWhereMatches(table, columns, wild_cards))


@app.post("/GetAllWhereIn/{table}/{column}/{search_parameters}", status_code=status.HTTP_200_OK)
def getAllWhereIn(table, columns, search_parameters):
    errorLogger(table)
    errorLogger(columns)
    errorLogger(search_parameters)

    successLogger(cursor, operations=operations.getAllWhereIn(table, columns, search_parameters))

@app.post("/GetAllWhereAndCount/{table}/{primary_column}/{secondary_column}/{search_parameter}", status_code=status.HTTP_200_OK)
def getAllWhereAndCount(table, primary_column, secondary_column, search_parameters):
    errorLogger(table)
    errorLogger(primary_column)
    errorLogger(secondary_column)
    errorLogger(search_parameters)

    successLogger(cursor, operations=operations.getAllWhereAndcount(table, primary_column, secondary_column, search_parameters))


@app.post("/GetAllWhereAverage/{table}/{column}", status_code=status.HTTP_200_OK)
def getAllWhereAndCount(table, column):
    errorLogger(table)
    errorLogger(column)

    successLogger(cursor, operations=operations.getAllWhereAndAverage(table, column))


@app.post("/GetAllGroupBy/{table}/{primary_column}/{secondary_column}", status_code=status.HTTP_200_OK)
def getAllWhereAndCount(table, primary_column, secondary_column):
    errorLogger(table)
    errorLogger(primary_column)
    errorLogger(secondary_column)
    
    successLogger(cursor, operations=operations.getAllGroupBy(table, primary_column, secondary_column))







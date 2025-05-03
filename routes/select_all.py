from fastapi import FastAPI, HTTPException, status
from middleware.errorlogger import errorLogger
from services.queries.selectors.select_all import SelectAll
import psycopg2 # type: ignore

connection = psycopg2.connect(dbname="akuko-uwa", user="postgres", password="dummy", host="localhost", port="5432")
cursor = connection.cursor()

app = FastAPI()
http_response = HTTPException()

## TODO: Improve error logger to avoid repetition
## TODO: Add selected DB Engine checker middleware one-level above this on API gateway

@app.post("/GetAll/{table}", status_code=status.HTTP_200_OK)
def getAll(table: str):

    errorLogger(table)
    operations = SelectAll()
    cursor.execute(operations)
    return cursor.fetchall()


@app.post("/GetAllOrderBy/{table}/{order}", status_code=status.HTTP_200_OK)
def getAllOrderBy(table: str, order: str):
    errorLogger(table)
    errorLogger(order)

    operations = SelectAll()
    cursor.execute(operations)
    return cursor.fetchall()
    
@app.post("/GetAllWithLimitAndOffset/{table}/{limit}/{offset}", status_code=status.HTTP_201_CREATED)
def getAllWithLimitAndOffset(table: str, limit: int, offset: int):
    errorLogger(table)
    errorLogger(limit)
    errorLogger(offset)

    operations = SelectAll()
    cursor.execute(operations)
    return cursor.fetchall()
    

@app.post("/GetAllWithLimit/{table}/{limit}", status_code=status.HTTP_201_CREATED)
def getAllWithLimit(table: str, limit: int):
    errorLogger(table)
    errorLogger(limit)

    operations = SelectAll()
    cursor.execute(operations)
    return cursor.fetchall()
    
   
    
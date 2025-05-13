from fastapi import FastAPI, HTTPException, status
from middleware.errorlogger import errorLogger
from middleware.success_logger import successLogger
from models.request_model import RequestModel
from services.queries.selectors.select_by_column import SelectByColumn
import psycopg2 # type: ignore

connection = psycopg2.connect(dbname="akuko-uwa", user="postgres", password="dummy", host="localhost", port="")
cursor = connection.cursor()

app = FastAPI()
http_response = HTTPException()
operations = SelectByColumn()


@app.post("/GetByColumns", status_code=status.HTTP_200_OK)
def getByColumns(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.columns)

    return operations.getByColumns(request.table, request.columns, cursor)


@app.post("/GetByColumnsAndOrderBy", status_code=status.HTTP_200_OK)
def getByColumnsOrderBy(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.columns)
    errorLogger(request.order)

    return operations.getByColumnsAndOrderBy(request.table, request.columns, request.order, cursor)


@app.post("/GetByColumnsAndLimit", status_code=status.HTTP_200_OK)
def getByColumnsAndLimit(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.columns)
    errorLogger(request.limit)

    return operations.getByColumnsAndLimit(request.table, request.columns, request.limit)
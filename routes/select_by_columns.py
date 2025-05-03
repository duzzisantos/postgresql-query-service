from fastapi import FastAPI, HTTPException, status
from middleware.errorlogger import errorLogger
from middleware.success_logger import successLogger
from services.queries.selectors.select_by_column import SelectByColumn
import psycopg2 # type: ignore

connection = psycopg2.connect(dbname="akuko-uwa", user="postgres", password="dummy", host="localhost", port="5432")
cursor = connection.cursor()

app = FastAPI()
http_response = HTTPException()
operations = SelectByColumn()


@app.post("/GetByColumns/{table}/{columns}", status_code=status.HTTP_200_OK)
def getByColumns(table: str, columns: list[str]):
    errorLogger(table)
    errorLogger(columns)

    successLogger(cursor=cursor, operations=operations.getByColumns(table, columns))


@app.post("/GetByColumnsAndOrderBy/{table}/{columns}/{order}", status_code=status.HTTP_200_OK)
def getByColumnsOrderBy(table: str, columns: list[str], order: str):
    errorLogger(table)
    errorLogger(columns)
    errorLogger(order)

    successLogger(cursor=cursor, operations=operations.getByColumnsAndOrderBy(table, columns, order))


@app.post("/GetByColumnsAndLimit/{table}/{columns}/{limit}", status_code=status.HTTP_200_OK)
def getByColumnsAndLimit(table: str, columns: list[str], limit: int):
    errorLogger(table)
    errorLogger(columns)
    errorLogger(limit)

    successLogger(cursor=cursor, operations=operations.getByColumnsAndLimit(table, columns, limit))
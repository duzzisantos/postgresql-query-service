from fastapi import APIRouter, status
from middleware.errorlogger import errorLogger
from models.request_model import RequestModel
from services.queries.selectors.select_by_column import SelectByColumn
from routes.connection_verify import client_configs

cursor = client_configs
select_by_column_router = APIRouter()
operations = SelectByColumn()


@select_by_column_router.post("/GetByColumns", status_code=status.HTTP_200_OK)
def getByColumns(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.columns)

    return operations.getByColumns(request.table, request.columns, cursor)


@select_by_column_router.post("/GetByColumnsAndOrderBy", status_code=status.HTTP_200_OK)
def getByColumnsOrderBy(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.columns)
    errorLogger(request.order)

    return operations.getByColumnsAndOrderBy(request.table, request.columns, request.order, cursor)


@select_by_column_router.post("/GetByColumnsAndLimit", status_code=status.HTTP_200_OK)
def getByColumnsAndLimit(request: RequestModel):
    errorLogger(request.table)
    errorLogger(request.columns)
    errorLogger(request.limit)

    return operations.getByColumnsAndLimit(request.table, request.columns, request.limit, cursor)
from fastapi import APIRouter, status
from middleware.errorlogger import errorLogger
from middleware.log_error import log_error
from models.request_model import RequestModel
from services.queries.selectors.select_by_column import SelectByColumn
from routes.connection_verify import connection_verify

cursor = connection_verify
select_by_column_router = APIRouter()
operations = SelectByColumn()


@select_by_column_router.post("/GetByColumns", status_code=status.HTTP_200_OK)
def getByColumns(request: RequestModel):
    log_error([request.table, request.columns])

    return operations.getByColumns(request.table, request.columns, cursor)


@select_by_column_router.post("/GetByColumnsAndOrderBy", status_code=status.HTTP_200_OK)
def getByColumnsOrderBy(request: RequestModel):
    log_error([request.table, request.columns, request.order])

    return operations.getByColumnsAndOrderBy(request.table, request.columns, request.order, cursor)


@select_by_column_router.post("/GetByColumnsAndLimit", status_code=status.HTTP_200_OK)
def getByColumnsAndLimit(request: RequestModel):
    log_error([request.table, request.columns, request.limit])

    return operations.getByColumnsAndLimit(request.table, request.columns, request.limit, cursor)
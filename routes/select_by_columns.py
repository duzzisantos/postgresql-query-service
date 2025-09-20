from fastapi import APIRouter, status
from models.request_model import RequestModel
from middleware.connection_state import get_connection
from utils.request import request

select_by_column_router = APIRouter()


@select_by_column_router.post("/GetByColumns", status_code=status.HTTP_200_OK)
def getByColumns(model: RequestModel):
    comma_separated_columns = ", ".join(model.columns)
    request("SELECT %s FROM %s", (comma_separated_columns, model.table))


@select_by_column_router.post("/GetByColumnsAndOrderBy", status_code=status.HTTP_200_OK)
def getByColumnsOrderBy(model: RequestModel):
    multi_cols = ", ".join(model.columns)
    request("SELECT % FROM %s ORDER BY %s", (multi_cols, model.table, model.order))


@select_by_column_router.post("/GetByColumnsAndLimit", status_code=status.HTTP_200_OK)
def getByColumnsAndLimit(model: RequestModel):
    multi_cols = ", ".join(model.columns)
    request("SELECT %s FROM %s LIMIT %s", (multi_cols, model.table, model.limit))
        
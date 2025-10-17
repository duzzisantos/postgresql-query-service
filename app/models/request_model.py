from pydantic import BaseModel
from typing import Optional
from datetime import date
  
class GetAll(BaseModel):
    table: str

class OrderBy(GetAll):
    order: str

class LimitAndOffset(GetAll):
    limit: int
    offset: int

class WithLimit(GetAll):
    limit: int

class AllWhere(GetAll):
    conditions: list[str]

class AllWhereOrderBy(AllWhere):
    order: str

class AllBetween(GetAll):
    column: str
    start: Optional[str | int | date]
    end: Optional[str | int | date]

class AllWhereMatches(GetAll):
    column: str
    wild_card: str | int

class AllWhereIn(GetAll):
    column: str
    search_parameters: Optional[list[str] | str | int]

class AllWhereAndCount(GetAll):
    primary_column: str
    secondary_column: str
    search_parameter: str | int

class AllWhereAverageModel(AllWhereIn):
    pass

class AllGroupByModel(GetAll):
    primary_column: str
    secondary_column: str


class ByColumns(GetAll):
    columns: list[str]

class ByColumnsAndOrder(ByColumns):
    order: str

class ByColumnsAndLimit(ByColumns):
    limit: int

class TableJoinModel(BaseModel):
    columns: list[str]
    primary_table: str
    secondary_table: str
    common_key: str

class SubQueryExists(BaseModel):
    primary_column: str
    primary_table: str
    sub_query_select: str
    sub_query_table: str
    sub_query_where_column: str
    sub_query_where_value: str

class CreateRow(BaseModel):
    columns: list[str]
    table: str
    values: list[str | int]

class CreateMany(CreateRow):
    columns: list[str]
    table: str
    values: list[list[str | int]]

class DeleteRow(BaseModel):
    table: str
    id: int | str
    primary_column: str

class DeleteMany(DeleteRow):
    table: str
    primary_key: list[int | str]

class DeleteByParams(AllWhere):
    conditions: list[str]

class UpdateRow(BaseModel):
    table: str
    primary_column: Optional[str]
    set_value: Optional[str | int | bool | date]
    secondary_column: str
    where_value: str

class UpdateMany(BaseModel):
    table: str
    set_columns: list[str]
    set_values: list[str | int | bool | date]
    where_value: str | int | bool | date
    where_column: str

class CreateTable(BaseModel):
    table_name: str
    column_names_with_properties: list[str]

class QueryDownload(BaseModel):
    query: str
    file_name: str
    recipient: Optional[str | list[str]]
    sender: str
    password: str
    role: Optional[str | list[str]]
    subject: str
    message: str
    email_server: str



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
    pass

class AllWhereMatches(GetAll):
    columns: list[str]
    wild_cards: list[str]

class AllWhereIn(GetAll):
    column: str
    search_parameters: Optional[list[str] | str | int]

class AllWhereAndCount(GetAll):
    primary_column: str
    secondary_column: str
    search_parameters: Optional[list[str] | str | int]

class AllWhereAverageModel(AllWhereIn):
    pass

class AllGroupByModel(AllWhereAndCount):
    pass


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
    join_type: str

class CreateRow(BaseModel):
    columns: list[str]
    table: str
    values: list[str] | list[tuple]

class CreateMany(CreateRow):
    pass

class DeleteRow(BaseModel):
    table: str
    primary_key: Optional[str | int]

class DeleteMany(DeleteRow):
    pass

class DeleteByParams(DeleteRow):
    parameters: list[str]
    columns: list[str]

class UpdateRow(BaseModel):
    table: str
    primary_column: Optional[str]
    set_value: Optional[str | int | bool | date]
    secondary_column: str
    where_value: str

class UpdateMany(UpdateRow):
    primary_columns: list[str]
    set_values: list[str | int | bool | date]


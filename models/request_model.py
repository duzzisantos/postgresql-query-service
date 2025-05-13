from pydantic import BaseModel
from typing import Optional, Union
from datetime import date

class RequestModel(BaseModel):
    table: Optional[str]
    values: Optional[Union[list[str] | list[tuple]]]
    column: Optional[str]
    columns: Optional[list[str]]
    primary_key: Optional[str]
    secondary_column: Optional[str]
    secondary_columns: Optional[list[str]]
    primary_column: Optional[str]
    primary_columns: Optional[list[str]]
    common_key: Optional[str]
    primary_table: Optional[str]
    secondary_table: Optional[str]
    join_type: Optional[str]
    cursor: function
    order: Optional[str]
    limit: Optional[int]
    offset: Optional[int]
    conditions: Optional[list[str]]
    query_range: Optional[Union[list[str | int]]]
    wild_cards: Optional[list[str]]
    search_parameters: Optional[Union[list[str] | str | int]]
    set_value: Optional[str]
    where_value: Optional[str]
    set_values: Optional[list[str | int | bool | date]]
    parameters: Optional[list[str]]
  


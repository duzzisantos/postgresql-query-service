from pydantic import BaseModel
from typing import Optional, Union
from datetime import date
import json
import inspect
  
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


def get_example_value(field_type):
    origin = getattr(field_type, '__origin__', None)
    if origin is Union:
        for arg in field_type.__args__:
            if arg != type(None):
                return get_example_value(arg)
    elif origin is list:
        sub_type = field_type.__args__[0]
        return [get_example_value(sub_type)]
    elif field_type == str:
        return "example_string"
    elif field_type == int:
        return 123
    elif field_type == bool:
        return True
    elif field_type == date:
        return "2023-01-01"
    return "example"

# Collect all BaseModel subclasses
models = [
    obj for name, obj in globals().items()
    if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj.__name__ != "BaseModel"
]

# Build Markdown blocks
markdown_blocks = []
for model in models:
    class_name = model.__name__
    route = f"/{class_name}"  # PascalCase route
    example = {}
    for field_name, field in model.__annotations__.items():
        example[field_name] = get_example_value(field)
    json_body = json.dumps(example, indent=2)
    
    block = (
        f"<details>\n"
        f"<summary><strong>POST {route}</strong></summary>\n\n"
        f"```json\n"
        f"{json_body}\n"
        f"```\n\n"
        f"</details>\n"
    )

    markdown_blocks.append(block)

# Output to file
with open("README_snippet.md", "w") as f:
    f.write("\n".join(markdown_blocks))

print("✅ Markdown saved to README_snippet.md")

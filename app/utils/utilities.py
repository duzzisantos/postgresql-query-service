from fastapi import HTTPException, status
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID

def manage_http_response(status: int, message: str | dict):
    return HTTPException(status_code=status, detail=message)

def json_safe(value):
    if isinstance(value, (Decimal, datetime, date, UUID)):
        return str(value)
    return value

def fetch_all_as_dict(cursor):
    status = cursor.statusmessage.strip()
    
    # Handle non-SELECT operations (INSERT, UPDATE, DELETE)
    if not status.startswith("SELECT"):
        return {
            "rows_affected": cursor.rowcount,
            "status_message": status
        }

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Single row result
    if len(rows) == 1:
        return {
            columns[i]: json_safe(value)
            for i, value in enumerate(rows[0])
        }

    # Multiple rows
    return [
        {
            columns[i]: json_safe(value)
            for i, value in enumerate(row)
        }
        for row in rows
    ]

## inner query builder for set colums with values
def set_items(model):
        if len(model.set_columns) != len(model.set_values):
            return None  # Return None if columns and values don't match

        set_statements = []
        for i in range(len(model.set_columns)):
            column = model.set_columns[i]
            value = model.set_values[i]
            # Format each pair as column = value
            if isinstance(value, str):
                set_statements.append(f"{column} = '{value}'")
            else:
                set_statements.append(f"{column} = {value}")

        return ", ".join(set_statements)


## return only true strings, so no integers allowed
def cleansed_string(string: str):
     result = []
     if string != "":
          for item in string:
               if not item.isnumeric():
                    result.append(item)
          return "".join(result)
          

          
          
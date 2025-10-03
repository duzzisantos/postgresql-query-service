from fastapi import HTTPException
def manage_http_response(status: int, message: str | dict):
    return HTTPException(status_code=status, detail=message)

def fetch_all_as_dict(cursor):
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

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

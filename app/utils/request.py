from app.middleware.connection_state import get_connection, release_connection
from fastapi import HTTPException, status
from psycopg2 import errors, sql
from app.utils.utilities import fetch_all_as_dict
from app.routes.observability import handle_logging


async def request(query, params=None):
    """
    Execute a query safely. `query` should be a psycopg2.sql.Composed/SQL object
    or a plain string only for static queries with no user input.
    `params` is passed to cursor.execute() for parameterized value binding.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if isinstance(query, (sql.Composed, sql.SQL)):
            cursor.execute(query, params)
        elif isinstance(query, str) and query.strip():
            cursor.execute(query, params)
        else:
            await handle_logging("error", "Empty Queries Not Allowed")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty Queries Not Allowed")

        data = {"operation": "database_query", "result": fetch_all_as_dict(cursor)}
        rows_length = len(data["result"]) if isinstance(data["result"], list) else 1
        await handle_logging("success", {"query_state": "Success", "rows": rows_length})
        return data

    except errors.ConnectionFailure:
        await handle_logging("error", "Service Unavailable. Check Connection Settings and Retry")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable. Check Connection Settings and Retry")
    except errors.UndefinedTable:
        await handle_logging("error", "Table Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table Not Found")
    except errors.DuplicateTable:
        await handle_logging("error", "Table Already Exists")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Table Already Exists")
    except errors.UniqueViolation:
        await handle_logging("error", "Row with unique primary key already exists")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Row with unique primary key already exists")
    except errors.SyntaxError:
        await handle_logging("error", "Syntax Error Occurred. Cannot Process Request")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Syntax Error Occurred. Cannot Process Request.")
    except errors.InternalError:
        await handle_logging("error", "Internal Server Error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    finally:
        cursor.close()
        release_connection(conn)

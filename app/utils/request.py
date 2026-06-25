from app.middleware.connection_state import get_connection, release_connection
from app.middleware.request_context import get_request_context
from fastapi import HTTPException, status
from psycopg2 import errors, sql
from app.utils.utilities import fetch_all_as_dict
from app.routes.observability import handle_logging


async def request(query, params=None):
    ctx = get_request_context()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if isinstance(query, (sql.Composed, sql.SQL)):
            cursor.execute(query, params)
        elif isinstance(query, str) and query.strip():
            cursor.execute(query, params)
        else:
            await handle_logging("error", "Empty Queries Not Allowed", http_status=400, **ctx)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty Queries Not Allowed")

        data = {"operation": "database_query", "result": fetch_all_as_dict(cursor)}
        rows_length = len(data["result"]) if isinstance(data["result"], list) else 1
        await handle_logging("success", f"Query OK — {rows_length} rows", http_status=200, **ctx)
        return data

    except errors.ConnectionFailure:
        await handle_logging("error", "Service Unavailable. Check Connection Settings and Retry", http_status=503, **ctx)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable. Check Connection Settings and Retry")
    except errors.UndefinedTable:
        await handle_logging("sql_error", "Table Not Found", http_status=404, **ctx)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table Not Found")
    except errors.DuplicateTable:
        await handle_logging("sql_error", "Table Already Exists", http_status=409, **ctx)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Table Already Exists")
    except errors.UniqueViolation:
        await handle_logging("sql_error", "Row with unique primary key already exists", http_status=409, **ctx)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Row with unique primary key already exists")
    except errors.SyntaxError:
        await handle_logging("sql_error", "Syntax Error Occurred. Cannot Process Request", http_status=422, **ctx)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Syntax Error Occurred. Cannot Process Request.")
    except errors.InternalError:
        await handle_logging("error", "Internal Server Error", http_status=500, **ctx)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    finally:
        cursor.close()
        release_connection(conn)

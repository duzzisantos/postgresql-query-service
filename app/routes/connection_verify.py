from fastapi import APIRouter, HTTPException
from app.middleware.connection_state import get_connection, release_connection
from app.middleware.request_context import get_request_context
from app.routes.observability import handle_logging
import psycopg2

connection_verify = APIRouter()


@connection_verify.post("/Connection")
async def checkConnection():
    ctx = get_request_context()
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        cursor.close()

        data = {
            "status": "OK",
            "message": "Connection established.",
            "test_query_result": result,
        }
        await handle_logging(
            "success", "Connection established", http_status=200, **ctx
        )
        return data

    except psycopg2.OperationalError:
        await handle_logging(
            "error",
            "Failed to connect to database. Check credentials",
            http_status=400,
            **ctx,
        )
        raise HTTPException(
            status_code=400,
            detail=f"Connection state: {conn.__getstate__()}. Details Failed to connect to database. Check credentials",
        )
    except Exception:
        await handle_logging(
            "error", "Unexpected error occurred", http_status=500, **ctx
        )
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    finally:
        if conn:
            release_connection(conn)

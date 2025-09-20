from fastapi import APIRouter, HTTPException
from middleware.errorlogger import errorLogger
from middleware.connection_state import get_connection
import psycopg2

connection_verify = APIRouter()
@connection_verify.post("/Connection")
async def checkConnection():
   
    try:
        cursor = get_connection().cursor()
        with cursor as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()

        return {
            "status": "OK",
            "message": "Connection established.",
            "test_query_result": result,
        }

    except psycopg2.OperationalError as e:
        errorLogger(str(e))
        raise HTTPException(status_code=400, detail="Failed to connect to database. Check credentials.")
    except Exception as e:
        errorLogger(str(e))
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

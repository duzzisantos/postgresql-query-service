from fastapi import APIRouter, HTTPException
from middleware.errorlogger import errorLogger
from middleware.connection_state import get_connection
from app.routes.observability import handle_logging

import psycopg2

connection_verify = APIRouter()
@connection_verify.post("/Connection")
async def checkConnection():
   
    try:
        cursor = get_connection().cursor()
        with cursor as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()

            data = {
            "status": "OK",
            "message": "Connection established.",
            "test_query_result": result,
           }
            
            await handle_logging("success", data)
            return data


    except psycopg2.OperationalError:
        await handle_logging("error", "Failed to connect to database. Check credentials")
        raise HTTPException(status_code=400, detail="Failed to connect to database. Check credentials.")
    except Exception:
        await handle_logging("error", "Unexpected error occurred.")
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    



from openpyxl import Workbook
from fastapi import APIRouter, HTTPException, status
from psycopg2 import errors
from app.middleware.connection_state import get_connection
from app.utils.utilities import fetch_all_as_dict
from app.routes.observability import handle_logging
from app.tasks.celery_app import send_weekly_query_report
from app.models.request_model import QueryDownload

queried_download_router = APIRouter()

@queried_download_router.post("/GetQueriedDownload", status_code=status.HTTP_200_OK)
async def get_queried_download(model: QueryDownload):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(model.query)
        query_result = fetch_all_as_dict(cursor)

        if not query_result:
            await handle_logging("error", "Queried Resource For Downloading Does Not Exist")
            raise HTTPException(status_code=404, detail="Queried Resource For Downloading Does Not Exist")

        ## Crontab schedule
        await send_weekly_query_report(model, query_result)
        
        await handle_logging("success", "Query Download and Email Dispatch Was SuccessFul")

    except errors.SyntaxError:
        await handle_logging("error", "Query Syntax Error For Downloading Occurred")
        raise HTTPException(status_code=422, detail="Query Syntax Error For Downloading Occurred")
    except errors.InternalError:
        await handle_logging("error", "Internal Server Error While Processing Queried Downloads")
        raise HTTPException(status_code=500, detail="Internal Server Error While Processing Queried Downloads")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        



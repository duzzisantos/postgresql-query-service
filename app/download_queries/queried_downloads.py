from fastapi import APIRouter, HTTPException, status, Depends
from psycopg2 import errors, sql
from app.middleware.connection_state import get_connection, release_connection
from app.middleware.no_injection import validate_identifier
from app.middleware.auth import require_api_key
from app.utils.utilities import fetch_all_as_dict
from app.routes.observability import handle_logging
from app.tasks.celery_app import send_query_report
from app.models.request_model import QueryDownload

queried_download_router = APIRouter(dependencies=[Depends(require_api_key)])


@queried_download_router.post("/GetQueriedDownload", status_code=status.HTTP_200_OK)
async def get_queried_download(model: QueryDownload):
    """
    Run a safe SELECT query, convert results to Excel, and email it via Celery.
    The raw query field is intentionally restricted to SELECT-only to prevent
    arbitrary DML/DDL through this endpoint.
    """
    stripped = model.query.strip().rstrip(";").strip()
    if not stripped.upper().startswith("SELECT"):
        raise HTTPException(status_code=422, detail="Only SELECT queries are allowed for download.")

    # Block dangerous keywords that shouldn't appear in a download query
    upper = stripped.upper()
    for forbidden in ("DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "EXEC", "CREATE"):
        if forbidden in upper:
            raise HTTPException(status_code=422, detail=f"Forbidden keyword '{forbidden}' in query.")

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(stripped)
        query_result = fetch_all_as_dict(cursor)
        cursor.close()

        if not query_result:
            await handle_logging("error", "Query returned no results for download")
            raise HTTPException(status_code=404, detail="Query returned no results")

        # Normalize to list for the Celery task
        rows = query_result if isinstance(query_result, list) else [query_result]

        # Dispatch via Celery (.delay queues it; the worker picks it up)
        send_query_report.delay(
            query_result=rows,
            recipient=model.recipient,
            subject=model.subject,
            message=model.message,
            sender=model.sender,
            password=model.password,
            email_server=model.email_server,
        )

        await handle_logging("success", "Query download queued for email dispatch")
        return {"status": "queued", "message": "Report is being generated and will be emailed shortly."}

    except errors.SyntaxError:
        await handle_logging("error", "Query Syntax Error For Downloading Occurred")
        raise HTTPException(status_code=422, detail="Query Syntax Error")
    except errors.InternalError:
        await handle_logging("error", "Internal Server Error While Processing Download")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if conn:
            release_connection(conn)

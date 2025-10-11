from openpyxl import Workbook
from fastapi import APIRouter, HTTPException, status
from psycopg2 import errors
from middleware.connection_state import get_connection
from utils.utilities import fetch_all_as_dict
from app.routes.observability import handle_logging
from io import BytesIO
from fastapi.responses import StreamingResponse
from models.request_model import QueryDownload
from models.emailing_model import SendQueryFileToEmail, EmailProperties

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

        workbook = Workbook()
        sheet = workbook.active
        headers = list(dict.fromkeys(key for instance in query_result for key in instance))
        sheet.append(headers)

        for row in query_result:
            sheet.append([row.get(h) for h in headers])

        # Save to in-memory stream
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        
        await handle_logging("success", "Query Download SuccessFul")
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={model.file_name}"}
        )

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
            

async def download_result():
    return await get_queried_download()




queried_download_router.post("/DispatchDownload", status_code=status.HTTP_200_OK)
async def dispatchDownload(model: EmailProperties):
    
    attachment = await download_result()
    email = SendQueryFileToEmail(model.recipient, model.sender, model.password, model.role,
                                  model.subject, model.message, model.email_server, attachment=attachment)
    
    return await email.send_to_recipients()



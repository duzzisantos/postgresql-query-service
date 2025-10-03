from openpyxl import Workbook
from fastapi import APIRouter, HTTPException, status
from psycopg2 import errors
from middleware.connection_state import get_connection
from utils.utilities import fetch_all_as_dict
from io import BytesIO
from fastapi.responses import StreamingResponse
from models.request_model import QueryDownload

queried_download_router = APIRouter()

@queried_download_router.post("/GetQueriedDownload", status_code=status.HTTP_200_OK)
async def get_queried_download(model: QueryDownload):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(model.query)
        query_result = fetch_all_as_dict(cursor)

        if not query_result:
            raise HTTPException(status_code=404, detail="Queried Resource Does Not Exist")

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

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={model.file_name}"}
        )

    except errors.SyntaxError:
        raise HTTPException(status_code=422, detail="Query Syntax Error Occurred")
    except errors.InternalError:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
        



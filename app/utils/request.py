from app.middleware.connection_state import get_connection
from fastapi import HTTPException, status
from psycopg2 import errors
from app.utils.utilities import fetch_all_as_dict
from app.routes.observability import handle_logging

async def request(query_template: str, variables: tuple[str | int | bool | tuple | list[str]]):
        cursor = get_connection().cursor()
        
        if query_template.__ne__(""):
            try:
                with cursor as cur:
                    cur.execute(query_template, variables)
                    data = {"operation": "database_query", "result": fetch_all_as_dict(cur)}
                    rows_length = len(data["result"])
                    await handle_logging("success", {"query_state": "Success", "rows": rows_length}) ## just log count - don't log potentially sensitive query row data
                    return data
                    
                    
            except errors.ConnectionFailure:
                await handle_logging("error", "Service Unavailable. Check Connection Settings and Retry") 
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable. Check Connection Settings and Retry")
            except errors.UndefinedTable:
                await handle_logging("error", "Table Not Found") 
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table Not Found")
            except errors.DuplicateTable:
                await handle_logging("error", "Table Already Exists. Duplicate Attempted") 
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Table Already Exists. Duplicate Attempted")
            except errors.UniqueViolation:
                await handle_logging("error", "Row with unique primary key already exists") 
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Row with unique primary key already exists")
            except errors.SyntaxError:
                await handle_logging("error", "Syntax Error Occured. Cannot Process Request") 
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Syntax Error Occured. Cannot Process Request.")
            except errors.InternalError:
                await handle_logging("error", "Internal Server Error") 
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
            
            finally:
                cursor.close()
        
        else:
            await handle_logging("error", "Empty Queries Not Allowed") 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty Queries Not Allowed")

 
from middleware.connection_state import get_connection
from fastapi import HTTPException, status
from psycopg2 import errors
from utils.utilities import fetch_all_as_dict

async def request(query_template: str, variables: tuple[str | int | bool | tuple | list[str]]):
    if(query_template.__ne__("") or query_template.__ne__(None)):

        cursor = get_connection().cursor()

        try:
            with cursor as cur:
                cur.execute(query_template, variables)
                print(fetch_all_as_dict(cur))
                
                
        except errors.ConnectionFailure: 
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable. Check Connection Settings and Retry")
        except errors.UndefinedTable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table Not Found")
        except errors.DuplicateTable:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Table Already Exists. Duplicate Attempted")
        except errors.UniqueViolation:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Row with unique primary key already exists")
        except errors.SyntaxError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Syntax Error Occured. Cannot Process Request.")
        except errors.InternalError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        
        finally:
            cursor.close()

    else:
        return {
            "error": "Query Template Can Neither Be Empty Nor Null"
        }
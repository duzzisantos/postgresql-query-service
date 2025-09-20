from middleware.connection_state import get_connection
from fastapi import HTTPException
from psycopg2 import errors

def request(query_template: str, variables: tuple[str | int | bool | tuple | list[str]]):
    if(query_template.__ne__("") or query_template.__ne__(None) or variables.count() == 0):

        cursor = get_connection().cursor()

        try:
            with cursor as cur:
                cur.execute(query_template, variables)
        
        ## plug-in your telemetry tools like prometheus/grafana etc for log tracking
        except errors.ConnectionFailure: 
            raise HTTPException(status_code=503, detail="Service Unavailable. Check Connection Settings and Retry")
        except errors.DatabaseError:
            raise HTTPException(status_code=503, detail="Service Unavailable. Check That Database Exists")
        except errors.UndefinedTable:
            raise HTTPException(status_code=404, detail="Table Not Found")
        except errors.SyntaxError:
            raise HTTPException(status_code=422, detail="Syntax Error Occured. Cannot Process Request.")
        
        finally:
            cursor.close()

    else:
        return {
            "error": "Query Template Can Neither Be Empty Nor Null"
        }
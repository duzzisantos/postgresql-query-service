from middleware.validate_params import validateParams
from middleware.no_injection import is_potential_sqli, validate_params_against_sqli
from fastapi import HTTPException

def errorLogger(params):
    if(validateParams(params)["result"] == False):
        ## TODO Append error message to list of error logs later using Prometheus => then ....
        raise HTTPException(status_code=422, detail=validateParams(params)["message"])
    else:
        for key, value in params.items():
            if(is_potential_sqli(value)):
              ## TODO Append error message to list of error logs later using Prometheus => then ....
              print("Key: " + key + " is causing potential sqli")
              raise HTTPException(status_code=422, detail=validate_params_against_sqli(params)["warning"])
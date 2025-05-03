from middleware.validate_params import validateParams
from middleware.no_injection import is_potential_sqli, validate_params_against_sqli
from fastapi import HTTPException

def errorLogger(params):
    if(validateParams(params)["result"] == False):
        ## TODO Append error message to list of error logs later using Prometheus => then ....
        raise HTTPException(status_code=400, detail=validateParams(params)["message"])
    elif(is_potential_sqli(params) or validate_params_against_sqli(params)):
        ## TODO Append error message to list of error logs later using Prometheus => then ....
        raise HTTPException(status_code=400, detail=validate_params_against_sqli(params)["warning"])
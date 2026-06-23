from app.middleware.validate_params import validate_params
from app.middleware.no_injection import is_potential_sqli
from fastapi import HTTPException


def error_logger(params: dict):
    validation = validate_params(params)
    if not validation["result"]:
        raise HTTPException(status_code=422, detail=validation["message"])

    for key, value in params.items():
        if isinstance(value, str) and is_potential_sqli(value):
            raise HTTPException(status_code=422, detail=f"Potential SQL injection in parameter: {key}")

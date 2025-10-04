import re
from fastapi import status, HTTPException
from psycopg2 import errors
from app.routes.observability import handle_logging
import datetime

SQLI_PATTERNS = [
    r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|EXEC|--|#|;)\b",
    r"' OR '1'='1",
    r"(?i)(\bor\b|\band\b)\s+\d+=\d+",
]

def get_validation_log(key: str, issues: str | list[str]):
    return {
            "timestamp": datetime.datetime.now().__str__(),
            "validation_warning": f"Validation failed! Unsupported content. Attempted SQLi attack using parameter: {key}.",
            "rejected_value": issues, 
            "status": True
            }


def is_potential_sqli(param: str) -> bool:
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, param, flags=re.IGNORECASE):
            return True
    return False


async def validate_params_against_sqli(params: dict):
    try:
        issues = []
        for key, value in params.items():
           if isinstance(value, str) and is_potential_sqli(value):
              await handle_logging("error", get_validation_log(key, value))
           elif isinstance(value, list) and len(value) != 0:
               for element in value:
                   if(is_potential_sqli(element)):
                       issues.append(element)
                       await handle_logging("error", get_validation_log(key, value))
    
        return issues
                       
    except errors.SyntaxError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation Error Occurred While Processing Request")


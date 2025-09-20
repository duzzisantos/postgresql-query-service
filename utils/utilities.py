from fastapi import HTTPException
def manage_http_response(status: int, message: str | dict):
    return HTTPException(status_code=status, detail=message)

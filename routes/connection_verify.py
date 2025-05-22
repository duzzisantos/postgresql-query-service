from fastapi import APIRouter, status
from middleware.errorlogger import errorLogger
from middleware.connection import Connection

connection_verify = APIRouter()
client_configs = None


@connection_verify.post("/Connection")
async def checkConnection(database: str, user: str, password: str):
    errorLogger({"database": database, "user": user, "password": password})
    connect = Connection(database, user, password)
    client_configs = connect.start_connection()

    return client_configs



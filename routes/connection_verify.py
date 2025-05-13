from fastapi import FastAPI, status
from middleware.errorlogger import errorLogger
from middleware.connection import Connection

connection_verify = FastAPI()
client_configs = {}

@connection_verify.post("/Connection", status_code=status.HTTP_200_OK)
async def checkConnection(dbname: str, user: str, password: str, host: str, port: str):
    errorLogger(dbname)
    errorLogger(user)
    errorLogger(password)
    errorLogger(host)
    errorLogger(port)

    connect = Connection(dbname, user, password, host, port)
    client_configs["cursor"] = connect.start_connection()

    return client_configs



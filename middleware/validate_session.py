from fastapi import HTTPException
from middleware.connection import Connection

def validate_session(session_id: str, stored_connections: dict):
    if session_id not in stored_connections:
        raise HTTPException(status_code=401, detail="Invalid Database Session")
    
    creds = stored_connections[session_id]
    connection = Connection(creds["database"], creds["user"], creds["password"]).start_connection()
    cursor = Connection(creds["database"], creds["user"], creds["password"]).start_connection()

    return {"conn": connection, "cursor": cursor}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.joiners import joiner_router
from routes.mutators import mutator_router
from routes.select_all import select_all_router
from routes.select_by_columns import select_by_column_router
from routes.connection_verify import connection_verify
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

app = FastAPI()
webhost = os.getenv("WEBHOST")
localhost = os.getenv("LOCALHOST")
origins = [
    localhost, webhost
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                       allow_methods=["POST, GET, DELETE, PUT, PATCH"], allow_headers=["*"])

app.include_router(connection_verify)
app.include_router(joiner_router)
app.include_router(mutator_router)
app.include_router(select_all_router)
app.include_router(select_by_column_router)

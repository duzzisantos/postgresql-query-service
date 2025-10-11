from fastapi import FastAPI
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
from app.routes.joiners import joiner_router
from app.routes.mutators import mutator_router
from app.routes.select_all import select_all_router
from app.routes.select_by_columns import select_by_column_router
from app.routes.tables import table_router
from app.routes.connection_verify import connection_verify
from app.download_queries.queried_downloads import queried_download_router
from app.routes.observability import log_router
from dotenv import load_dotenv
import uvicorn
import os
load_dotenv()

app = FastAPI()
webhost = os.getenv("WEBHOST")
localhost = os.getenv("LOCALHOST")
port = os.getenv("PORT")
postgres_url = os.getenv("POSTGRES_URL")

origins = [
    localhost, webhost
]

@app.get("/")
async def root():
    return {"message": "enter /docs to view API documentation"}

def main():
    conn = psycopg2.connect(postgres_url)
    query_sql = 'SELECT VERSION()'
    cursor = conn.cursor()
    cursor.execute(query_sql)

    pg_version = cursor.fetchone()[0]
    print({"postgresql_version": pg_version})
    


app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                        allow_methods=["POST, GET"], allow_headers=["*"])


## Included routes
app.include_router(log_router)
app.include_router(connection_verify)
app.include_router(joiner_router)
app.include_router(mutator_router)
app.include_router(select_all_router)
app.include_router(select_by_column_router)
app.include_router(table_router)
app.include_router(queried_download_router)


if __name__  == "__main__":
    main()
    uvicorn.run("app.main:app", host=localhost, port=int(port))

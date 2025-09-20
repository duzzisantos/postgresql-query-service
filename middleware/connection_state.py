import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
    conn.autocommit = True
    return conn



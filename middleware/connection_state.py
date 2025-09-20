import psycopg2
import os

def get_connection():
    conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
    conn.autocommit = True
    return conn



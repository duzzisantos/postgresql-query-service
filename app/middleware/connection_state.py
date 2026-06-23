from psycopg2 import pool
from app.core.config import settings

# Connection pool — reuses connections instead of opening one per request
_pool = None


def _get_pool():
    global _pool
    if _pool is None or _pool.closed:
        _pool = pool.ThreadedConnectionPool(minconn=2, maxconn=10, dsn=settings.POSTGRES_URL)
    return _pool


def get_connection():
    conn = _get_pool().getconn()
    conn.autocommit = True
    return conn


def release_connection(conn):
    try:
        _get_pool().putconn(conn)
    except Exception:
        pass

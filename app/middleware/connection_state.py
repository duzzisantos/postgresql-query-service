from psycopg2 import pool
from app.core.config import settings

_pool = None


def _get_dsn():
    dsn = settings.POSTGRES_URL
    if dsn and "connect_timeout" not in dsn:
        sep = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{sep}connect_timeout=10"
    return dsn


def _get_pool():
    global _pool
    if _pool is None or _pool.closed:
        _pool = pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=_get_dsn())
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

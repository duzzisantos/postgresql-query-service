from loguru import logger
from fastapi import APIRouter, status, Depends
from app.middleware.connection_state import get_connection, release_connection
from app.middleware.auth import require_api_key
import sys

log_router = APIRouter(dependencies=[Depends(require_api_key)])

OBSERVABILITY_SCHEMA = [
    "id SERIAL PRIMARY KEY",
    "http_status INTEGER NOT NULL",
    "log_type VARCHAR(20) NOT NULL",
    "endpoint VARCHAR(255) NOT NULL",
    "source_ip VARCHAR(45)",
    "destination_ip VARCHAR(45)",
    "message TEXT",
    "created_at TIMESTAMP DEFAULT now()",
]

SORTABLE_COLUMNS = {"id", "http_status", "log_type", "endpoint", "source_ip", "destination_ip", "message", "created_at"}

_table_created = False


def _ensure_table():
    global _table_created
    if _table_created:
        return
    conn = get_connection()
    cursor = conn.cursor()
    try:
        col_defs = ", ".join(OBSERVABILITY_SCHEMA)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS observability_logs ({col_defs})")
        conn.commit()
        _table_created = True
    except Exception as e:
        conn.rollback()
        logger.warning(f"Failed to create observability_logs table: {e}")
    finally:
        cursor.close()
        release_connection(conn)


async def handle_logging(
    log_type: str,
    message: str,
    http_status: int = 200,
    endpoint: str = "",
    source_ip: str = "",
    destination_ip: str = "",
):
    if log_type == "error" or log_type == "sql_error":
        logger.error(message)
    else:
        logger.success(message)

    try:
        _ensure_table()
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO observability_logs
                   (http_status, log_type, endpoint, source_ip, destination_ip, message)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (http_status, log_type, endpoint, source_ip, destination_ip, str(message)),
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.warning(f"Failed to persist log: {e}")
        finally:
            cursor.close()
            release_connection(conn)
    except Exception:
        pass


@log_router.get("/GetLogs", status_code=status.HTTP_200_OK)
async def get_logs(
    limit: int = 25,
    offset: int = 0,
    log_type: str = "",
    endpoint: str = "",
    http_status: int | None = None,
    search: str = "",
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    if sort_by not in SORTABLE_COLUMNS:
        sort_by = "created_at"
    direction = "ASC" if sort_order.lower() == "asc" else "DESC"

    where_clauses = []
    params: list = []

    if log_type:
        where_clauses.append("log_type = %s")
        params.append(log_type)
    if endpoint:
        where_clauses.append("endpoint ILIKE %s")
        params.append(f"%{endpoint}%")
    if http_status is not None:
        where_clauses.append("http_status = %s")
        params.append(http_status)
    if search:
        where_clauses.append("message ILIKE %s")
        params.append(f"%{search}%")

    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM observability_logs{where_sql}", params)
        total = cursor.fetchone()[0]

        query = f"SELECT * FROM observability_logs{where_sql} ORDER BY {sort_by} {direction} LIMIT %s OFFSET %s"
        cursor.execute(query, params + [limit, offset])

        cols = [desc[0] for desc in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        return {"operation": "get_logs", "result": rows, "total": total}
    finally:
        cursor.close()
        release_connection(conn)


@log_router.get("/GetLogStats", status_code=status.HTTP_200_OK)
async def get_log_stats():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                DATE_TRUNC('hour', created_at) AS time_bucket,
                log_type,
                COUNT(*) AS count
            FROM observability_logs
            GROUP BY time_bucket, log_type
            ORDER BY time_bucket ASC
        """)
        cols = [desc[0] for desc in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        return {"operation": "get_log_stats", "result": rows}
    finally:
        cursor.close()
        release_connection(conn)

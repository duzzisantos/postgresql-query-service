from fastapi import HTTPException
from psycopg2 import sql
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID


def manage_http_response(status: int, message: str | dict):
    return HTTPException(status_code=status, detail=message)


def json_safe(value):
    if isinstance(value, (Decimal, datetime, date, UUID)):
        return str(value)
    return value


def fetch_all_as_dict(cursor):
    status_msg = cursor.statusmessage.strip()

    if not status_msg.startswith("SELECT"):
        return {
            "rows_affected": cursor.rowcount,
            "status_message": status_msg,
        }

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    if len(rows) == 1:
        return {columns[i]: json_safe(value) for i, value in enumerate(rows[0])}

    return [{columns[i]: json_safe(value) for i, value in enumerate(row)} for row in rows]


def build_set_clause(columns: list[str], values: list):
    """Build a SET clause using sql.Identifier for column names and %s for values."""
    if len(columns) != len(values):
        return None, None

    parts = []
    for col in columns:
        parts.append(sql.SQL("{} = %s").format(sql.Identifier(col)))

    return sql.SQL(", ").join(parts), tuple(values)

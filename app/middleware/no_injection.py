import re
from fastapi import HTTPException, status
from app.routes.observability import handle_logging
import datetime

# Allowlist: identifiers (table/column names) must be alphanumeric + underscores only.
# This is the FIRST line of defense. The SECOND is psycopg2.sql.Identifier() quoting.
SAFE_IDENTIFIER = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

# Known SQLi payload patterns — catches obvious attacks in string *values*
SQLI_VALUE_PATTERNS = [
    r"'\s*(OR|AND)\s+.*=",
    r";\s*(DROP|ALTER|TRUNCATE|EXEC)\b",
    r"--\s*$",
    r"/\*.*\*/",
    r"UNION\s+(ALL\s+)?SELECT",
]

_compiled_value_patterns = [re.compile(p, re.IGNORECASE) for p in SQLI_VALUE_PATTERNS]


def validate_identifier(name: str, label: str = "identifier"):
    """Reject any table/column name that isn't a plain SQL identifier."""
    if not SAFE_IDENTIFIER.match(name):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid {label}: '{name}'. Only letters, digits, and underscores are allowed.",
        )


def validate_identifier_list(names: list[str], label: str = "column"):
    for name in names:
        validate_identifier(name, label)


def is_potential_sqli(value: str) -> bool:
    for pattern in _compiled_value_patterns:
        if pattern.search(value):
            return True
    return False


async def validate_params_against_sqli(params: dict):
    """Check string values in request body for SQLi payloads."""
    issues = []
    for key, value in params.items():
        if isinstance(value, str) and is_potential_sqli(value):
            issues.append(key)
            await handle_logging("error", {
                "timestamp": str(datetime.datetime.now()),
                "validation_warning": f"Potential SQLi in parameter: {key}",
                "status": True,
            })
        elif isinstance(value, list):
            for element in value:
                if isinstance(element, str) and is_potential_sqli(element):
                    issues.append(key)
                    await handle_logging("error", {
                        "timestamp": str(datetime.datetime.now()),
                        "validation_warning": f"Potential SQLi in list parameter: {key}",
                        "status": True,
                    })

    if issues:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Request rejected — suspicious content in fields: {', '.join(issues)}",
        )

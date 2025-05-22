import re

SQLI_PATTERNS = [
    r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|EXEC|--|#|;)\b",
    r"' OR '1'='1",
    r"(?i)(\bor\b|\band\b)\s+\d+=\d+",
]


def is_potential_sqli(param: str) -> bool:
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, param, flags=re.IGNORECASE):
            return True
    return False

def validate_params_against_sqli(params: dict) -> dict:
    for key, value in params.items():
        if isinstance(value, str) and is_potential_sqli(value):
            return {"warning": f"Validation failed! Unsupported content. Attempted SQLi attack using parameter: {key}.", "rejected_value": value, "status": True}

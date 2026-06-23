def validate_params(params) -> dict:
    if isinstance(params, str) and params == "":
        return {"message": "Validation failed: empty string", "result": False}
    if isinstance(params, (list, tuple)) and len(params) == 0:
        return {"message": "Validation failed: empty list", "result": False}
    if params is None:
        return {"message": "Validation failed: None value", "result": False}
    return {"message": "Validation passed", "result": True}

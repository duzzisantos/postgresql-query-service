from app.middleware.errorlogger import error_logger


def log_error(params: list[dict]):
    for param in params:
        if param:
            error_logger(param)

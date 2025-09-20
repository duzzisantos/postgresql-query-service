from middleware.errorlogger import errorLogger

def log_error(params: list[str]):
    if(len(params) != 0):
       for param in params:
           return errorLogger(param)
    else:
        return
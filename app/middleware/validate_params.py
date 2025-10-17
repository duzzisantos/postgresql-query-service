def validateParams(params: str | int | list[str]) -> dict:
    if (params.__eq__("")):
        return {"message": f"Validation failed! {params} returned an empty string", "result": False}
    elif(len(params) == 0):
         return {"message": f"Validation failed {params} returned an empty array of strings", "result": False}
    elif(not params):
         return {"message": f"Validation failed {params} returned no integer", "result": False}
    else:
         return {"message": f"Validation succeeded {params} successfully validated", "result": True}
    


def validateConnectionParams(dbname: str, user: str, password: str, host: str, port: str) -> dict | bool:
     if(dbname.__ne__("") and user.__ne__("") and password.__ne__("") and host.__ne__("") and port.__ne__("") and len(int(port)) == 4):
          return True
     return {"message": f"Connection parameters were missing.", "result": False}

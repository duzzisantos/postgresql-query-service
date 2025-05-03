def validateParams(params: str | int | list[str]):
    if (type(params).__eq__(str) and params.__eq__("")):
        return {"message": f"Validation failed! {params} returned an empty string", "result": False}
    elif(type(params).__eq__(list[str]) and len(params).__eq__(0)):
         return {"message": f"Validation failed {params} returned an empty array of strings", "result": False}
    elif(type(params).__eq__(int) and not params):
         return {"message": f"Validation failed {params} returned no integer", "result": False}
    else:
         return {"message": f"Validation succeeded {params} successfully validated", "result": True}

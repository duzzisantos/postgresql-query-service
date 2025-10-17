from fastapi import APIRouter, status, HTTPException
from app.models.request_model import CreateRow, CreateMany, DeleteRow, DeleteMany, DeleteByParams, UpdateMany, UpdateRow
from app.middleware.connection_state import get_connection
from app.utils.utilities import fetch_all_as_dict, set_items
from app.routes.observability import handle_logging
from app.utils.request import request
from datetime import date
from app.middleware.no_injection import validate_params_against_sqli

mutator_router = APIRouter()
cursor = get_connection().cursor()
CACHE_TIME = int(1200)

@mutator_router.post("/CreateOne") ## ca marche
async def createOne(model: CreateRow):
    await validate_params_against_sqli(dict(model))
    multi_cols = ", ".join(model.columns)
    
    query = f"INSERT INTO {model.table} ({multi_cols}) VALUES {tuple(model.values)}"
    result = await request(query, (model.table, model.columns, model.values))
    return result

 

@mutator_router.post("/CreateMany") ## ca marche
async def createMany(model: CreateMany):
    await validate_params_against_sqli(dict(model))
    multi_cols = ", ".join(model.columns)
    
    def tupulize_values():
        result = []
        for row in model.values:
            result.append(tuple(row))
        return result


    dynamic_values = ", ".join(str(t) for t in tupulize_values())

    query = f"INSERT INTO {model.table} ({multi_cols}) VALUES {dynamic_values}"
    res = await request(query, (model.table, model.columns, model.values))
    return res

    

@mutator_router.post("/DeleteById") ## ca marche
async def deleteById(model: DeleteRow):
   await validate_params_against_sqli(dict(model))
   result = await request(f"DELETE FROM {model.table} WHERE {model.primary_column} = {int(model.id)}", ())
   return result

  

@mutator_router.post("/DeleteMany") ## ca marche
async def deleteMany(model: DeleteMany):
    await validate_params_against_sqli(dict(model))
    result = await request(f"DELETE FROM {model.table}", ())
    return result
 

@mutator_router.post("/UpdateOne") ## ca marche
async def updateOne(model: UpdateRow):
    await validate_params_against_sqli(dict(model))
    result = await request((f"UPDATE {model.table} SET {model.secondary_column} = {model.set_value} WHERE {model.primary_column} =  {model.where_value}"), ())
    return result


@mutator_router.post("/UpdateMany",  status_code=status.HTTP_200_OK) ## ca marche
async def updateMany(model: UpdateMany):
    await validate_params_against_sqli(dict(model))
    try:
        with cursor as cur:
            query = f"UPDATE {model.table} SET {set_items(model)} WHERE {model.where_column} = '{model.where_value}'"
            cur.execute(query)
            await handle_logging("dml", fetch_all_as_dict(cur))
            return fetch_all_as_dict(cur)
    
    except Exception:
            await handle_logging("error", "Updating many resources not successfully carried out. Check parameters") 
            raise HTTPException(status_code=500, detail='Updating many resources not successfully carried out. Check parameters')
    finally:
        cursor.close()


    



from fastapi import APIRouter, status, HTTPException
from models.request_model import RequestModel
from middleware.connection_state import get_connection
from utils.request import request
from datetime import date

mutator_router = APIRouter()
cursor = get_connection().cursor()

@mutator_router.post("/CreateOne")
async def createOne(model: RequestModel):
    multi_cols = ", ".join(model.columns)
    placeholders = ", ".join(["%s"] * len(model.columns))
    query = f"INSERT INTO {model.table} ({multi_cols}) VALUES ({placeholders})"

    request(query, model.values)
       
    

@mutator_router.post("/CreateMany")
async def createMany(model: RequestModel):
    multi_cols = ", ".join(model.columns)
    placeholders = ", ".join(["%s"] * len(model.columns))
    query = f"INSERT INTO {model.table} ({multi_cols}) VALUES ({placeholders})"
    request(query, model.values)

    

@mutator_router.post("/DeleteById")
async def deleteById(model: RequestModel):
    request("DELETE FROM %s WHERE %s", (model.table, model.primary_key))
  

@mutator_router.post("/DeleteMany")
async def deleteMany(model: RequestModel):
    request("DELETE FROM %s", (model.table))

@mutator_router.post("/DeleteByParameters")
async def deleteMany(model: RequestModel):
    multi_cols = " AND ".join(model.columns).join(" = ").join(model.parameters)
    request("DELETE FROM %s WHERE %s", (model.table, multi_cols))

@mutator_router.post("/UpdateOne")
async def updateOne(model: RequestModel):
    request(("UPDATE %s SET %s = %s WHERE %s =  %s", (model.table, 
                                                                model.primary_column, 
                                                                model.set_value, 
                                                                model.secondary_column, model.where_value)))


@mutator_router.post("/UpdateMany",  status_code=status.HTTP_200_OK)
async def updateMany(model: RequestModel):
    try:
        with cursor as cur:
            for column in model.primary_columns:
              for value in model.set_values:
                if (isinstance(str, value) or isinstance(int, value) or isinstance(bool, value) or isinstance(date, value)):
                   cur.execute("UPDATE %s SET %s WHERE %s = %s", (model.table, ", ".join(f"{column} = {value}"), model.secondary_column, model.where_value))
    
    except Exception: 
            raise HTTPException(status_code=500, detail='Updating many resources not successfully carried out. Check parameters')
    finally:
        cursor.close()


    



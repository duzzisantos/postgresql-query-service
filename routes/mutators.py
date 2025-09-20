from fastapi import APIRouter, status, HTTPException
from query_builders.mutators.creators import Creators
from query_builders.mutators.deleters import Deleters
from query_builders.mutators.updaters import Updaters
from models.request_model import RequestModel
from middleware.connection_state import get_connection
from datetime import date

mutator_router = APIRouter()

insert = Creators()
remove = Deleters()
update = Updaters()

@mutator_router.post("/CreateOne")
async def createOne(model: RequestModel):
  
    cursor = get_connection().cursor()
  
    try:
        with cursor as cur:
            multi_cols = ", ".join(model.columns)
            placeholders = ", ".join(["%s"] * len(model.columns))
            query = f"INSERT INTO {model.table} ({multi_cols}) VALUES ({placeholders})"
            cur.execute(query, model.values)
            result = cur.fetchone()
            return {"create_one": result}
    except Exception: 
            raise HTTPException(status_code=500, detail='Internal Server Error')
    finally: 
        cursor.close()
       
    

@mutator_router.post("/CreateMany")
async def createMany(model: RequestModel):
    cursor = get_connection().cursor()

    try:
        with cursor as cur:
            multi_cols = ", ".join(model.columns)
            placeholders = ", ".join(["%s"] * len(model.columns))
            query = f"INSERT INTO {model.table} ({multi_cols}) VALUES ({placeholders})"
            cur.execute(query, model.values)
            result = cur.fetchone()
            return {"create_one": result}
    except: 
            raise HTTPException(status_code=500, detail='Internal Server Error')
    
    finally: 
        cursor.close()
    

@mutator_router.post("/DeleteById")
async def deleteById(model: RequestModel):
    cursor = get_connection().cursor()
    try:
        with cursor as cur:
            cur.execute("DELETE FROM %s WHERE %s", (model.table, model.primary_key))
    except Exception: 
            raise HTTPException(status_code=400, detail='Bad Request')
    finally:
        cursor.close()

@mutator_router.post("/DeleteMany")
async def deleteMany(model: RequestModel):
    cursor = get_connection().cursor()
    try:
        with cursor as cur:
            cur.execute("DELETE FROM %s", (model.table))
    except: 
            raise HTTPException(status_code=500, detail='Unable to delete many resources.')
    finally:
        cursor.execute()

@mutator_router.post("/DeleteByParameters")
async def deleteMany(model: RequestModel):
    cursor = get_connection().cursor()
    try:
        with cursor as cur:
            multi_cols = " AND ".join(model.columns).join(" = ").join(model.parameters)
            cur.execute("DELETE FROM %s WHERE %s", (model.table, multi_cols))
    except Exception: 
            raise HTTPException(status_code=500, detail='Either parameters do not exist or columns and table name are wrong')
    finally:
        cursor.close()

@mutator_router.post("/UpdateOne")
async def updateOne(model: RequestModel):
    cursor = get_connection().cursor()
    try:
       with cursor as cur:
           cur.execute("UPDATE %s SET %s = %s WHERE %s =  %s", (model.table, 
                                                                model.primary_column, 
                                                                model.set_value, 
                                                                model.secondary_column, model.where_value))
    
    except Exception: 
            raise HTTPException(status_code=500, detail='Internal Server Error')                                                              
    finally:
        cursor.close()
        


@mutator_router.post("/UpdateMany",  status_code=status.HTTP_200_OK)
async def updateMany(model: RequestModel):
    cursor = get_connection().cursor()
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


    



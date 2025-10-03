from fastapi import APIRouter, status, HTTPException
from models.request_model import GetAll, OrderBy, LimitAndOffset, WithLimit, AllWhere, AllBetween, AllGroupByModel
from models.request_model import AllWhereIn, AllWhereAverageModel, AllWhereAndCount, AllWhereMatches, AllWhereOrderBy
from middleware.connection_state import get_connection
from middleware.no_injection import validate_params_against_sqli
from utils.request import request
from utils.utilities import fetch_all_as_dict
from psycopg2 import sql

select_all_router = APIRouter()
cursor = get_connection().cursor()
CACHE_TIME = int(1200)

@select_all_router.post("/GetAll", status_code=status.HTTP_200_OK) ##ça marche
async def getAll(model: GetAll):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT * FROM {model.table}", (model.table))
   


@select_all_router.post("/GetAllOrderBy", status_code=status.HTTP_200_OK) ##ça marche
async def getAllOrderBy(model: OrderBy):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT * FROM {model.table} ORDER BY {model.order}", ())
   

    
@select_all_router.post("/GetAllWithLimitAndOffset", status_code=status.HTTP_200_OK) ##ça marche
async def getAllWithLimitAndOffset(model: LimitAndOffset):
     await validate_params_against_sqli(dict(model))
     query = f"SELECT * FROM {model.table} LIMIT {model.limit} OFFSET {model.offset}"
     await request(query, ())
 
    

@select_all_router.post("/GetAllWithLimit", status_code=status.HTTP_200_OK) ##ça marche
async def getAllWithLimit(model: WithLimit):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT * FROM {model.table} LIMIT {model.limit}", ())

    
   
@select_all_router.post("/GetAllWhere", status_code=status.HTTP_200_OK) ##ça marche
async def getAllWhere(model: AllWhere):
    await validate_params_against_sqli(dict(model))

    try:
        with cursor as cur:
            query_conditions = ''

            if(len(model.conditions) == 1):
                query_conditions = " ".join(model.conditions)
                cur.execute(f"SELECT * FROM {model.table} WHERE {query_conditions}", ())
                print(fetch_all_as_dict(cur))
                
            elif(len(model.conditions) > 1):
                query_conditions = " AND ".join(model.conditions)
                cur.execute(f"SELECT * FROM {model.table} WHERE {query_conditions}", ())
                print(fetch_all_as_dict(cur))
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()



@select_all_router.post("/GetAllWhereAndOrderBy", status_code=status.HTTP_200_OK) ## on doit refactorer pour ça marche
async def getAllWhereAndOrderBy(model: AllWhereOrderBy):
    await validate_params_against_sqli(dict(model))

    try:
        with cursor as cur:
            query_conditions = ''

            if(len(model.conditions) == 1):
                query_conditions = " ".join(model.conditions)
                cur.execute(f"SELECT * FROM {model.table} WHERE {query_conditions} ORDER BY {model.order}", ())
                print(fetch_all_as_dict(cur))
            else:
                query_conditions = " AND ".join(model.conditions)
                print(query_conditions)
                cur.execute(f"SELECT * FROM {model.table} WHERE {query_conditions} ORDER BY {model.order}", ())
                print(fetch_all_as_dict(cur))
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllBetween", status_code=status.HTTP_200_OK) ## ca marche
async def getAllBetween(model: AllBetween):
    await validate_params_against_sqli(dict(model))
  
    try:
        with cursor as cur:
          query = f"SELECT * FROM {model.table} WHERE {model.column} BETWEEN {model.start} AND {model.end}"
          cur.execute(query, ())
          print(fetch_all_as_dict(cur))
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()


@select_all_router.post("/GetAllWhereMatches", status_code=status.HTTP_200_OK)
async def getAllWhereMatches(model: AllWhereMatches):
   
    await validate_params_against_sqli(dict(model))
    dynamic_wildcard = int(model.wild_card) if isinstance(model.wild_card, int) else f"'{model.wild_card}'"

    try:
        with cursor as cur:
            cur.execute(f"SELECT * FROM {model.table} WHERE {model.column} LIKE {dynamic_wildcard}", ())
            print(fetch_all_as_dict(cur))
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllWhereIn", status_code=status.HTTP_200_OK) ## ca marche
async def getAllWhereIn(model: AllWhereIn):
    await validate_params_against_sqli(dict(model))
    joined_str = tuple(model.search_parameters)
  
    await request(f"SELECT * FROM {model.table} WHERE {model.column} IN {joined_str}", ())
    


@select_all_router.post("/GetAllWhereAndCount", status_code=status.HTTP_200_OK) ## ca marche
async def getAllWhereAndCount(model: AllWhereAndCount):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT COUNT({model.primary_column}) FROM {model.table} WHERE {model.secondary_column} = '{model.search_parameter}'", ())
    

@select_all_router.post("/GetAllWhereAverage", status_code=status.HTTP_200_OK) ## ca marche
async def getAllWhereAndAverage(model: AllWhereAverageModel):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT AVG({model.column})::NUMERIC(10,2) FROM {model.table}", (model.table, model.column))
   


@select_all_router.post("/GetAllGroupBy", status_code=status.HTTP_200_OK) ## ca marche
async def getAllWhereAndGroupBy(model: AllGroupByModel):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT {model.secondary_column}, COUNT({model.primary_column}) FROM {model.table} GROUP BY {model.secondary_column}", ())
    






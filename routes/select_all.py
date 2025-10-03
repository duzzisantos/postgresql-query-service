from fastapi import APIRouter, status, HTTPException
from models.request_model import GetAll, OrderBy, LimitAndOffset, WithLimit, AllWhere, AllBetween, AllGroupByModel
from models.request_model import AllWhereIn, AllWhereAverageModel, AllWhereAndCount, AllWhereMatches, AllWhereOrderBy
from middleware.connection_state import get_connection
from middleware.no_injection import validate_params_against_sqli
from utils.request import request
from psycopg2 import sql

select_all_router = APIRouter()
cursor = get_connection().cursor()
CACHE_TIME = int(1200)

@select_all_router.post("/GetAll", status_code=status.HTTP_200_OK)
async def getAll(model: GetAll):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT * FROM {model.table}", (model.table))
   


@select_all_router.post("/GetAllOrderBy", status_code=status.HTTP_200_OK)
async def getAllOrderBy(model: OrderBy):
    await validate_params_against_sqli(dict(model))
    await request(f"SELECT * FROM {model.table} ORDER BY {model.order}", None)
   

    
@select_all_router.post("/GetAllWithLimitAndOffset", status_code=status.HTTP_200_OK)
async def getAllWithLimitAndOffset(model: LimitAndOffset):
     await validate_params_against_sqli(dict(model))
     query = sql.SQL("SELECT * FROM {table} LIMIT %s OFFSET %s").format(table=sql.Identifier(model.table))
     await request(query, (model.limit, model.offset,))
 
    

@select_all_router.post("/GetAllWithLimit", status_code=status.HTTP_200_OK)
async def getAllWithLimit(model: WithLimit):
    await validate_params_against_sqli(dict(model))
    await request("SELECT * FROM %s LIMIT %s;", (model.table, model.limit))

    
   
@select_all_router.post("/GetAllWhere", status_code=status.HTTP_200_OK)
async def getAllWhere(model: AllWhere):
    await validate_params_against_sqli(dict(model))
    result
    try:
        with cursor as cur:
            query_conditions = ''

            if(len(model.conditions) == 1):
                query_conditions = " ".join(model.conditions)
                cur.execute("SELECT * FROM %s WHERE %s", (model.table, query_conditions))
                result = cur.fetchall()
                
            elif(len(model.conditions) > 1):
                query_conditions = " AND ".join(model.conditions)
                cur.execute("SELECT * FROM %s WHERE %s", (model.table, query_conditions))
                result = cur.fetchall()
        return result
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllWhereAndOrderBy", status_code=status.HTTP_200_OK)
async def getAllWhereAndOrderBy(model: AllWhereOrderBy):
    await validate_params_against_sqli(dict(model))
    result

    try:
        with cursor as cur:
            query_conditions = ''

            if(len(model.conditions) == 1):
                query_conditions = " ".join(model.conditions)
                cur.execute("SELECT * FROM %s WHERE %s ORDER BY %s", (model.table, query_conditions, model.order))
                result = cur.fetchall()
            elif(len(model.conditions) > 1):
                query_conditions = " AND ".join(model.conditions)
                cur.execute("SELECT * FROM %s WHERE %s ORDER BY %s", (model.table, query_conditions, model.order))
                result = cur.fetchall()
        return result
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllBetween", status_code=status.HTTP_200_OK)
async def getAllBetween(model: AllBetween):
    await validate_params_against_sqli(dict(model))
    result

    try:
        with cursor as cur:

            if(len(range) == 2):
                cur.execute("SELECT * FROM %s BETWEEN %s AND %s", (model.table, range[0], range[1]))
                result = cur.fetchall()
                return result
            else:
                return None
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()


@select_all_router.post("/GetAllWhereMatches", status_code=status.HTTP_200_OK)
async def getAllWhereMatches(model: AllWhereMatches):
    await validate_params_against_sqli(dict(model))
    result

    try:
        with cursor as cur:

            if(len(model.columns).__eq__(1) and len(model.wild_cards).__eq__(1)):
                cur.execute("SELECT * FROM %s WHERE %s LIKE %s", (model.table, model.columns[0], model.wild_cards[0]))
                result = cur.fetchall()
            elif(len(model.columns).__ge__(2) and len(model.wild_cards).__ge__(2)):
                for column in model.columns:
                 for wild_card in model.wild_cards:
                     
                     joint_query_conditions = f" {column} LIKE {wild_card}"
                cur.execute(f"SELECT * FROM %s WHERE {" AND ".join(joint_query_conditions)}", (model.table, joint_query_conditions))
                result = cur.fetchall()
            return result   
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllWhereIn", status_code=status.HTTP_200_OK)
async def getAllWhereIn(model: AllWhereIn):
    await validate_params_against_sqli(dict(model))
    joined_str = ", ".join(model.search_parameters)
    await request("SELECT * FROM %s WHERE %s IN %s", (model.table, model.column, joined_str))
    


@select_all_router.post("/GetAllWhereAndCount", status_code=status.HTTP_200_OK)
async def getAllWhereAndCount(model: AllWhereAndCount):
    await validate_params_against_sqli(dict(model))
    await request("SELECT COUNT(%s) * FROM %s WHERE %s = %s ORDER BY %s", (model.table, model.primary_column, model.secondary_column, model.search_parameters))
    

@select_all_router.post("/GetAllWhereAverage", status_code=status.HTTP_200_OK)
async def getAllWhereAndAverage(model: AllWhereAverageModel):
    await validate_params_against_sqli(dict(model))
    await request("SELECT AVG(%s)::NUMERIC(10,2) FROM %s", (model.table, model.column))
   


@select_all_router.post("/GetAllGroupBy", status_code=status.HTTP_200_OK)
async def getAllWhereAndGroupBy(model: AllGroupByModel):
    await validate_params_against_sqli(dict(model))
    await request("SELECT COUNT(%s), %s FROM %s GROUP BY %s", (model.primary_column, model.secondary_column, model.table))
    






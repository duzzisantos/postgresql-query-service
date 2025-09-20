from fastapi import APIRouter, status, HTTPException
from models.request_model import RequestModel
from middleware.connection_state import get_connection
from utils.request import request


select_all_router = APIRouter()
cursor = get_connection().cursor()

@select_all_router.post("/GetAll", status_code=status.HTTP_200_OK)
async def getAll(model: RequestModel):
    request("SELECT * FROM %s", (model.table))


@select_all_router.post("/GetAllOrderBy", status_code=status.HTTP_200_OK)
async def getAllOrderBy(model: RequestModel):
    request("SELECT * FROM %s ORDER BY %s", (model.table, model.order))

    
@select_all_router.post("/GetAllWithLimitAndOffset", status_code=status.HTTP_200_OK)
async def getAllWithLimitAndOffset(model: RequestModel):
    request("SELECT * FROM %s LIMIT %s OFFSET %s", (model.table, model.limit, model.offset))
    

@select_all_router.post("/GetAllWithLimit", status_code=status.HTTP_200_OK)
async def getAllWithLimit(model: RequestModel):
    request("SELECT * FROM %s LIMIT %s;", (model.table, model.limit))
    
   
@select_all_router.post("/GetAllWhere", status_code=status.HTTP_200_OK)
def getAllWhere(model: RequestModel):
    try:
        with cursor as cur:
            query_conditions = ''

            if(len(model.conditions) == 1):
                query_conditions = " ".join(model.conditions)
                return cur.execute("SELECT * FROM %s WHERE %s", (model.table, query_conditions))
            elif(len(model.conditions) > 1):
                query_conditions = " AND ".join(model.conditions)
                return cur.execute("SELECT * FROM %s WHERE %s", (model.table, query_conditions))
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllWhereAndOrderBy", status_code=status.HTTP_200_OK)
async def getAllWhereAndOrderBy(model: RequestModel):

    try:
        with cursor as cur:
            query_conditions = ''

            if(len(model.conditions) == 1):
                query_conditions = " ".join(model.conditions)
                return cur.execute("SELECT * FROM %s WHERE %s ORDER BY %s", (model.table, query_conditions, model.order))
            elif(len(model.conditions) > 1):
                query_conditions = " AND ".join(model.conditions)
                return cur.execute("SELECT * FROM %s WHERE %s ORDER BY %s", (model.table, query_conditions, model.order))
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllBetween", status_code=status.HTTP_200_OK)
async def getAllBetween(model: RequestModel):

    try:
        with cursor as cur:

            if(len(range) == 2):
                return cur.execute("SELECT * FROM %s BETWEEN %s AND %s", (model.table, range[0], range[1]))
            else:
                return None
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()


@select_all_router.post("/GetAllWhereMatches", status_code=status.HTTP_200_OK)
async def getAllWhereMatches(model: RequestModel):

    try:
        with cursor as cur:

            if(len(model.columns).__eq__(1) and len(model.wild_cards).__eq__(1)):
                return cur.execute("SELECT * FROM %s WHERE %s LIKE %s", (model.table, model.columns[0], model.wild_cards[0]))
            elif(len(model.columns).__ge__(2) and len(model.wild_cards).__ge__(2)):
                for column in model.columns:
                 for wild_card in model.wild_cards:
                     
                     joint_query_conditions = f" {column} LIKE {wild_card}"
                return cur.execute(f"SELECT * FROM %s WHERE {" AND ".join(joint_query_conditions)}", (model.table, joint_query_conditions))   
    
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
    finally:
        cursor.close()

@select_all_router.post("/GetAllWhereIn", status_code=status.HTTP_200_OK)
async def getAllWhereIn(model: RequestModel):

    joined_str = ", ".join(model.search_parameters)
    request("SELECT * FROM %s WHERE %s IN %s", (model.table, model.column, joined_str))


@select_all_router.post("/GetAllWhereAndCount", status_code=status.HTTP_200_OK)
async def getAllWhereAndCount(model: RequestModel):

    request("SELECT COUNT(%s) * FROM %s WHERE %s = %s ORDER BY %s", (model.table, model.primary_column, model.secondary_column, model.search_parameters))

@select_all_router.post("/GetAllWhereAverage", status_code=status.HTTP_200_OK)
def getAllWhereAndAverage(model: RequestModel):

    request("SELECT AVG(%s)::NUMERIC(10,2) FROM %s", (model.table, model.column))


@select_all_router.post("/GetAllGroupBy", status_code=status.HTTP_200_OK)
def getAllWhereAndGroupBy(model: RequestModel):
    
    request("SELECT COUNT(%s), %s FROM %s GROUP BY %s", (model.primary_column, model.secondary_column, model.table))






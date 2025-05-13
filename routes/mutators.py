from fastapi import FastAPI, status
from middleware.errorlogger import errorLogger
from query_builders.mutators.creators import Creators
from query_builders.mutators.deleters import Deleters
from query_builders.mutators.updaters import Updaters
from models.request_model import RequestModel
from routes.connection_verify import client_configs

## Refactor error logger
mutator_router = FastAPI()
cursor = client_configs['cursor']

insert = Creators()
remove = Deleters()
update = Updaters()

@mutator_router.post("/CreateOne", status_code=status.HTTP_200_OK)
async def createOne(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.columns)
    errorLogger(model.values)

    return insert.createOne(model.table, model.columns, model.values, cursor)

@mutator_router.post("/CreateMany", status_code=status.HTTP_200_OK)
async def createMany(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.columns)
    errorLogger(model.values)

    return insert.createMany(model.table, model.columns, model.values, cursor)

@mutator_router.post("/DeleteById", status_code=status.HTTP_200_OK)
async def deleteById(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.primary_key)

    return remove.deleteById(model.table, model.primary_key, cursor)

@mutator_router.post("/DeleteMany", status_code=status.HTTP_200_OK)
async def deleteMany(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.columns)
    errorLogger(model.parameters)

    return remove.deleteMany(model.table, model.columns, model.parameters, cursor)

@mutator_router.post("/DeleteByParameters", status_code=status.HTTP_200_OK)
async def deleteMany(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.columns)
    errorLogger(model.parameters)

    return remove.deleteByParameters(model.table, model.columns, model.parameters, cursor)

@mutator_router.post("/UpdateOne", status_code=status.HTTP_200_OK)
async def updateOne(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.primary_column)
    errorLogger(model.secondary_column)
    errorLogger(model.set_value)
    errorLogger(model.where_value)
    
    return update.updateOne(model.table, model.primary_column,
                             model.secondary_column, model.set_value, model.where_value, cursor)


@mutator_router.post("/UpdateMany",  status_code=status.HTTP_200_OK)
async def updateMany(model: RequestModel):
    errorLogger(model.table)
    errorLogger(model.primary_columns)
    errorLogger(model.secondary_column)
    errorLogger(model.set_values)
    errorLogger(model.where_value)

    return update.updateMany(model.table, model.primary_columns,
                             model.secondary_column, model.set_values, model.where_value, cursor)


    



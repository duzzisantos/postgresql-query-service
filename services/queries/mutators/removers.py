from query_builders.mutators.deleters import Deleters

query = Deleters()
class Delete():

    def deleteById(table:str, primary_key: str, cursor: function):
        return query.deleteById(table, primary_key, cursor)
    
    def deleteMany(table: str, columns: list[str], parameters: list[str], cursor: function):
        return query.deleteMany(table, columns, parameters, cursor)
    
    def deleteByParameters(table: str, columns: list[str], parameters: list[str], cursor: function):
        return query.deleteByParameters(table, columns, parameters, cursor)
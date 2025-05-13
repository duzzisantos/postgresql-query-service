from query_builders.mutators.creators import Creators

query = Creators()
class Create():

    def createOne(table: str, columns: list[str], values: list[str], cursor: function) -> function:
        return query.createOne(table, columns, values, cursor)
    
    def createMany(table: str, columns: list[str], values: list[tuple], cursor: function) -> function:
        return query.createMany(table, columns, values, cursor)
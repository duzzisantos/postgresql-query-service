from query_builders.mutators.updaters import Updaters

query = Updaters()
class Update():

    def updateOne(table: str, primary_column: str, secondary_column: str, set_value: str, where_value: str, cursor: function ):
        return query.updateOne(table, primary_column, secondary_column, set_value, where_value, cursor)
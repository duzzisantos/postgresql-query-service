from query_builders.mutators.updaters import Updaters
from datetime import date
query = Updaters()
class Update():

    def updateOne(table: str, primary_column: str, secondary_column: str, set_value: str, where_value: str, cursor: function ):
        return query.updateOne(table, primary_column, secondary_column, set_value, where_value, cursor)
    
    def updateMany(table: str, primary_columns: list[str], secondary_column: str, set_values: list[str | int | bool | date], where_value: str):
        return query.updateMany(table, primary_columns, secondary_column, set_values, where_value)
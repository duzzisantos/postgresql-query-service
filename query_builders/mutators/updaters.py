from datetime import date

class Updaters:
    def updateOne(table: str, primary_column: str, secondary_column: str, set_value: str, where_value: str, cursor: function):
        return cursor.execute("UPDATE %s SET %s = %s WHERE %s =  %s", (table, primary_column, set_value, secondary_column, where_value ))
    
  
    def updateMany(table: str, primary_columns: list[str], secondary_column: str, set_values: c, where_value: str, cursor: function):
        for column in primary_columns:
            for value in set_values:
               if (isinstance(str, value) or isinstance(int, value) or isinstance(bool, value) or isinstance(date, value)):
                  return cursor.execute("UPDATE %s SET %s WHERE %s = %s", (table, ", ".join(f"{column} = {value}"), secondary_column, where_value))
    

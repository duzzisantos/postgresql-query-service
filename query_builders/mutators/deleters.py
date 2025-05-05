class Deleters:
    def deleteById(table, primary_key: str, cursor: function):
        return cursor.execute("DELETE FROM %s WHERE %s", (table, primary_key))
    
    def deleteMany(table: str, cursor: function):
        return cursor.execute("DELETE FROM %s", (table))
    
    def deleteByParameters(table: str, columns: list[str], parameters: list[str], cursor: function):
        multi_cols = " AND ".join(columns).join(" = ").join(parameters) ## Would need refactoring
        return cursor.execute("DELETE FROM %s WHERE %s", (table, multi_cols))
class Deleters:
    def deleteById(table: str, primary_key: str, cursor: dict):
        return cursor.execute("DELETE FROM %s WHERE %s", (table, primary_key))
    
    def deleteMany(table: str, cursor: dict):
        return cursor.execute("DELETE FROM %s", (table))
    
    def deleteByParameters(table: str, columns: list[str], parameters: list[str], cursor: dict):
        multi_cols = " AND ".join(columns).join(" = ").join(parameters) ## Would need refactoring
        return cursor.execute("DELETE FROM %s WHERE %s", (table, multi_cols))
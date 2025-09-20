class Creators:
    def createOne(table: str, columns: list[str], values: list[str], cursor):
        multi_cols = ", ".join(columns)
        vals = ", ".join(values)
        cursor.execute("INSERT INTO %s (%s) VALUES (%s)", (table, multi_cols, vals))
    

    def createMany(table: str, columns: list[str], values: list[tuple], cursor):
        multi_cols = ", ".join(columns)
        multi_vals = ", ".join(values)
        cursor.execute("INSERT INTO %s (%s) VALUES (%s)", (table, multi_cols, multi_vals))
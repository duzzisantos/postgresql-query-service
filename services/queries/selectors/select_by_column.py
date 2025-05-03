from query_builders.selectors import select_queries

query = select_queries.SelectQueries()

class SelectByColumn:
    def getByColumns(table: str, columns: list[str]):
        return query.selectByColumns(table, columns)
    
    def getByColumnsAndOrderBy(table: str, columns: list[str], order: str):
        return query.selectByColumnsAndOrderBy(table, columns, order)
    
    def getByColumnsAndLimit(table: str, columns: list[str], limit: int):
        return query.selectByColumnsAndLimit(table, columns, limit)
from query_builders.selectors.select_queries import SelectQueries

query = SelectQueries()
class SelectAll():
    
    def getAll(table: str):
        return query.selectAll(table)

    def getAllOrderBy(table: str, order: str):
        return query.selectAllOrderBy(table, order)

    def getAllWithLimitAndOffset(table: str, limit: int, offset: int):
        return query.selectAllWithLimitAndOffset(table, limit, offset)

    def getAllWithLimit(table: str, limit: int):
        return query.selectAllWithLimit(table, limit)

    def getAllWhere(table: str, conditions: list[str]):
        return query.selectAllWhere(table, conditions)

    def getAllWhereAndOrderBy(table: str, conditions: list[str], order: str):
        return query.selectAllWhereAndOrderBy(table, conditions, order)

    def getAllBetween(table: str, range: list[str | int]):
        return query.selectAllBetween(table, range)

    def getAllWhereMatches(table: str, columns: list[str], wild_cards: list[str]):
        return query.selectAllWhereMatches(table, columns, wild_cards)

    def getAllWhereIn(table: str, column: str, search_parameters: list[str]):
        return query.selectAllWhereIn(table, column, search_parameters)

    def getAllWhereAndcount(table: str, primary_column: str, secondary_column: str, search_parameters: str | int):
        return query.selectAllWhereAndCount(table, primary_column, secondary_column, search_parameters)

    def getAllWhereAndAverage(table: str, column: str):
        return query.selectAllWhereAndAverage(table, column)

    def getAllGroupBy(table: str, primary_column: str, secondary_column: str):
        return query.selectAllGroupBy(table, primary_column, secondary_column)
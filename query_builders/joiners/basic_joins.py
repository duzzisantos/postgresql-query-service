from joiners.joiner_util import use_joiner

class BasicJoin:
    def innerJoin(columns: list[str], join_type: str, primary_table: str, secondary_table: str, common_key: str, cursor: function):
        return use_joiner(columns, join_type, primary_table, secondary_table, common_key, cursor)
    
    def leftJoin(columns: list[str], join_type: str, primary_table: str, secondary_table: str, common_key: str, cursor: function):
        return use_joiner(columns, join_type, primary_table, secondary_table, common_key, cursor)
    
    def rightJoin(columns: list[str], join_type: str, primary_table: str, secondary_table: str, common_key: str, cursor: function):
        return use_joiner(columns, join_type, primary_table, secondary_table, common_key, cursor)
    
    def fullJoin(columns: list[str], join_type: str, primary_table: str, secondary_table: str, common_key: str, cursor: function):
        return use_joiner(columns, join_type, primary_table, secondary_table, common_key, cursor)
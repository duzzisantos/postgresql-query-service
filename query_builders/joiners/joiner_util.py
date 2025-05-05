class JoinerUtils:
    
    def use_joiner(columns: list[str], join_type: str, primary_table: str, secondary_table: str, common_key: str, cursor: function):
            multi_cols = ", ".join(columns)
            return cursor.execute("SELECT %s FROM %s %s JOIN %s ON %s  = %s", 
                                (multi_cols, primary_table, join_type, secondary_table, primary_table[common_key],
                                    secondary_table[common_key]))
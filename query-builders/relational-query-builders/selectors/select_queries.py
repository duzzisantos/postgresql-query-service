class SelectQueries:
        
       ## General select statements
        def selectAll(table: str):
            return f"SELECT * FROM {table};"
        
        def selectAllOrderBy(table: str, order: str):
            return f"SELECT * FROM {table} ORDER BY {order};"
        
        def selectAllWithLimitAndOffset(table: str, limit: int, offset: int):
            return f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset};"
        
        def selectAllWithLimit(table: str, limit: int):
            return f"SELECT * FROM {table} LIMIT {limit};"
        
        def selectAllWhere(table: str, conditions: list[str]):
            query_conditions = ''

            if(len(conditions) == 1):
                query_conditions = " ".join(conditions)
                return f"SELECT * FROM {table} WHERE {query_conditions};"
            elif(len(conditions) > 1):
                query_conditions = " AND ".join(conditions)
                return f"SELECT * FROM {table} WHERE {query_conditions};"
        
        def selectAllWhereAndOrderBy(table: str, conditions: list[str], order: int):
            query_conditions = ''

            if(len(conditions) == 1):
                query_conditions = " ".join(conditions)
                return f"SELECT * FROM {table} WHERE {query_conditions} ORDER BY {order};"
            elif(len(conditions) > 1):
                query_conditions = " AND ".join(conditions)
                return f"SELECT * FROM {table} WHERE {query_conditions} ORDER BY {order};"
            
        def selectAllBetween(table: str, range: list[str | int]):
            if(len(range) == 2):
                return f"SELECT * FROM {table} BETWEEN {range[0]} AND {range[1]};"
            else:
                return None
        
        def selectAllWhereMatches(table: str, columns: list[str], wild_cards: list[str]):
            if(len(columns).__eq__(1) and len(wild_cards).__eq__(1)):
                return f"SELECT * FROM {table} WHERE {columns[0]} LIKE {wild_cards[0]};"
            elif(len(columns).__ge__(2) and len(wild_cards).__ge__(2)):
                for column in columns:
                 for wild_card in wild_cards:
                     
                     joint_query_conditions = f" {column} LIKE {wild_card}"
                return f"SELECT * FROM {table} WHERE {" AND ".join(joint_query_conditions)};"      
                  
        def selectAllWhereIn(table: str, column: str, search_parameters: list[str]):
            return f"SELECT * FROM {table} WHERE {column} IN ({", ".join(search_parameters)});"
        
        def selectAllWhereAndCount(table: str, primary_column: str, secondary_column: str, search_parameter: str | int):
            return f"SELECT COUNT({primary_column}) * FROM {table} WHERE {secondary_column} = {search_parameter} ORDER BY {secondary_column};"
        
        def selectAllWhereAndAverage(table: str, column: str):
            return f"SELECT AVG({column})::NUMERIC(10,2) FROM {table};"
        
        def selectAllGroupBy(table: str, primary_column: str, secondary_column: str):
            return f"SELECT COUNT({primary_column}), {secondary_column} FROM {table} GROUP BY {secondary_column}"
            
        
            
        ## Specific column selectors

        def selectByColumns(table: str, columns: list[str]):
            comma_separated_columns = ", ".join(columns)

            return f"SELECT {comma_separated_columns} FROM {table};"
        
        def selectByColumnsAndOrderBy(table: str, columns: list[str], order: str):
            return f"SELECT {", ".join(columns)} FROM {table} ORDER BY {order};"
        
        def selectByColumnsAndLimit(table: str, columns: list[str], limit: int):
            return f"SELECT {", ".join(columns)} FROM {table} LIMIT {limit};"
        
      



        



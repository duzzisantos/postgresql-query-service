class SelectQueries:
        
       ## General select statements
        def selectAll(table: str, cursor: dict):
            return cursor.execute("SELECT * FROM %s", (table))
        
        def selectAllOrderBy(table: str, order: str, cursor: dict):
            return cursor.execute("SELECT * FROM %s ORDER BY %s", (table, order))
        
        def selectAllWithLimitAndOffset(table: str, limit: int, offset: int, cursor: dict):
            return cursor.execute("SELECT * FROM %s LIMIT %s OFFSET %s", (table, limit, offset))
        
        def selectAllWithLimit(table: str, limit: int, cursor: dict):
            return cursor.execute("SELECT * FROM %s LIMIT %s;", (table, limit))
        
        def selectAllWhere(table: str, conditions: list[str], cursor: dict):
            query_conditions = ''

            if(len(conditions) == 1):
                query_conditions = " ".join(conditions)
                return cursor.execute("SELECT * FROM %s WHERE %s", (table, query_conditions))
            elif(len(conditions) > 1):
                query_conditions = " AND ".join(conditions)
                return cursor.execute("SELECT * FROM %s WHERE %s", (table, query_conditions))
        
        def selectAllWhereAndOrderBy(table: str, conditions: list[str], order: str, cursor: dict):
            query_conditions = ''

            if(len(conditions) == 1):
                query_conditions = " ".join(conditions)
                return cursor.execute("SELECT * FROM %s WHERE %s ORDER BY %s", (table, query_conditions, order))
            elif(len(conditions) > 1):
                query_conditions = " AND ".join(conditions)
                return cursor.execute("SELECT * FROM %s WHERE %s ORDER BY %s", (table, query_conditions, order))
            
        def selectAllBetween(table: str, range: list[str | int], cursor: dict):
            if(len(range) == 2):
                return cursor.execute("SELECT * FROM %s BETWEEN %s AND %s", (table, range[0], range[1]))
            else:
                return None
        
        def selectAllWhereMatches(table: str, columns: list[str], wild_cards: list[str], cursor: dict):
            if(len(columns).__eq__(1) and len(wild_cards).__eq__(1)):
                return cursor.execute("SELECT * FROM %s WHERE %s LIKE %s", (table, columns[0], wild_cards[0]))
            elif(len(columns).__ge__(2) and len(wild_cards).__ge__(2)):
                for column in columns:
                 for wild_card in wild_cards:
                     
                     joint_query_conditions = f" {column} LIKE {wild_card}"
                return cursor.execute(f"SELECT * FROM %s WHERE {" AND ".join(joint_query_conditions)}", (table, joint_query_conditions))   
                  
        def selectAllWhereIn(table: str, column: str, search_parameters: list[str], cursor: dict):
            joined_str = ", ".join(search_parameters)
            return cursor.execute("SELECT * FROM %s WHERE %s IN %s", (table, column, joined_str))
        
        def selectAllWhereAndCount(table: str, primary_column: str, secondary_column: str, search_parameter: str | int, cursor: dict):
            return cursor.execute("SELECT COUNT(%s) * FROM %s WHERE %s = %s ORDER BY %s", (table, primary_column, secondary_column, search_parameter))
        
        def selectAllWhereAndAverage(table: str, column: str, cursor):
            return cursor.execute("SELECT AVG(%s)::NUMERIC(10,2) FROM %s", (table, column))
        
        def selectAllGroupBy(table: str, primary_column: str, secondary_column: str, cursor: dict):
            return cursor.execute("SELECT COUNT(%s), %s FROM %s GROUP BY %s", (primary_column, secondary_column, table))
            
        
            
        ## Specific column selectors

        def selectByColumns(table: str, columns: list[str], cursor: dict):
            comma_separated_columns = ", ".join(columns)
            return cursor.execute("SELECT %s FROM %s", (comma_separated_columns, table))
        
        def selectByColumnsAndOrderBy(table: str, columns: list[str], order: str, cursor: dict):
            multi_cols = ", ".join(columns)
            return cursor.execute("SELECT % FROM %s ORDER BY %s", (multi_cols, table, order))
        
        def selectByColumnsAndLimit(table: str, columns: list[str], limit: int, cursor: dict):
            multi_cols = ", ".join(columns)
            return cursor.execute("SELECT %s FROM %s LIMIT %s", (multi_cols, table, limit))
        
      



        



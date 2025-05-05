from joiners.joiner_util import use_joiner

class BasicJoin():
    def __init__(self, columns: list[str], join_type: str, primary_table, secondary_table, common_key: str, cursor: function):
        self.columns = columns
        self.join_type = join_type
        self.primary_table = primary_table
        self.secondary_table = secondary_table
        self.common_key = common_key
        self.cursor = cursor
        self.use_joiner = use_joiner(self.columns, self.join_type, self.primary_table, self.secondary_table, self.common_key, self.cursor)

    

    def innerJoin(self) -> function:
            return self.use_joiner
        
    def leftJoin(self) -> function:
            return self.use_joiner
        
    def rightJoin(self) -> function:
            return self.use_joiner
        
    def fullJoin(self) -> function:
            return self.use_joiner


        
        


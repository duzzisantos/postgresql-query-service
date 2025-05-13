from query_builders.joiners.basic_joins import BasicJoin

query = BasicJoin()
class Joiners():

    def getInnerJoin():
        return query.innerJoin()
    
    def getleftJoin():
        return query.leftJoin()
    
    def getRightJoin():
        return query.rightJoin()
    
    def getFullJoin():
        return query.fullJoin()
  
import psycopg2 # type: ignore


class Connection():
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def start_connection(self):
        
        connection = psycopg2.connect(self.dbname, self.user, self.password, self.host, self.port)
        cursor = connection.cursor()
        return cursor


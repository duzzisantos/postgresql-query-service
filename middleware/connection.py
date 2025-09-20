
import psycopg2

class Connection():
    def __init__(self, dbname: str, user: str, password: str):
        self.dbname = dbname
        self.user = user
        self.password = password

    def start_connection(self):
        connection = psycopg2.connect(
            database=self.dbname,
            user=self.user,
            password=self.password
        )
        return connection.cursor()

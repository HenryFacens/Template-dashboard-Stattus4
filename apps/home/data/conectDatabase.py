from django.db import connections

class DataBase:
    def __init__(self, connection_name) -> None:
        self.connection_name = connection_name

    
    def execute(self,query):
        with connections[self.connection_name].cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
    def get_cursor(self):
        return connections[self.connection_name].cursor()
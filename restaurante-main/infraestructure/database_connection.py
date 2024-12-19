from infraestructure.mysql_connection import MySQLConnection
from credentials_db import user, password, database, host

def get_connection():
    return MySQLConnection(host, user, password, database)

import sqlite3
from sqlite3 import Error

class Database:
    """"The class which connects the blockchain with the database,
     and performs all database actions """

    def create_connection(db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            conn.close()
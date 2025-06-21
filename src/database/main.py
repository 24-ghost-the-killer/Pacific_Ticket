import mysql.connector
import os
class Database():
    @staticmethod
    def connect():
        try:
            return mysql.connector.connect(
                host=os.getenv('DATABASE_HOST', ''),
                user=os.getenv('DATABASE_USER', ''),
                password=os.getenv('DATABASE_PASS', ''),
                database=os.getenv('DATABASE_DATA', '')
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            return None
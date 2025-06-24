import mysql.connector
import os
class Database:
    @staticmethod
    def connect():
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'root'),
                password=os.getenv('DATABASE_PASS', ''),
                database=os.getenv('DATABASE_DATA', 'pacific_database'),
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            return None
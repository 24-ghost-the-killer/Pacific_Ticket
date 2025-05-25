import mysql.connector
import os

class Database():
    def connect():
        return mysql.connector.connect(
            host=os.getenv('DATABASE_HOST', ''),
            user=os.getenv('DATABASE_USER', ''),
            password=os.getenv('DATABASE_PASS', ''),
            database=os.getenv('DATABASE_DATA', '')
        )

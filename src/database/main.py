import mysql.connector
import os
class Database():
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host=os.getenv('DATABASE_HOST', ''),
            user=os.getenv('DATABASE_USER', ''),
            password=os.getenv('DATABASE_PASS', ''),
            database=os.getenv('DATABASE_DATA', '')
        )
    
    @staticmethod
    def setting(name):
        try: 
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT value FROM settings WHERE name = %s", (name,))
                    result = cursor.fetchone()
                    if result:
                        return result['value']
                    else:
                        return None
        except Exception as e:
            print(f"Error in Database.setting: {e}")
            return None
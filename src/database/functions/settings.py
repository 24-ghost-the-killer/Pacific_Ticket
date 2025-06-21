from src.database.main import Database
class DatabaseSettings:
    @staticmethod
    def get(name):
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
        
    @staticmethod
    def getall():
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT name, value, disabled FROM settings")
                    return [
                        {
                            'name': row['name'],
                            'value': row['value'],
                            'disabled': row['disabled'],
                        }
                        for row in cursor.fetchall()
                    ]
        except Exception as e:
            print(f"Error in Database.settings: {e}")
            return []
        
    @staticmethod
    def update(name, value):
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "UPDATE settings SET value = %s WHERE name = %s",
                        (value, name)
                    )
                    conn.commit()
        except Exception as e:
            print(f"Error in Database.update_setting: {e}")
            return False
        return True
from src.database.main import Database
from functools import lru_cache

@lru_cache(maxsize=32)
class TicketDatabase():
    @staticmethod
    def create(data={
        'channel_name': None,
        'channel_id': None,
        'owner_username': None,
        'owner_id': None,
        'category': None
    }):
        try: 
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "INSERT INTO tickets (channel_name, channel_id, owner_username, owner_id, category) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (
                            data['channel_name'], 
                            data['channel_id'],
                            data['owner_username'], 
                            data['owner_id'], 
                            data['category']
                        )
                    )
                    conn.commit()
        except Exception as e:
            print(f"Error in TicketDatabase.create: {e}")
            return None

    @staticmethod
    def get(data={
        'channel_id': None
    }):
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT * FROM tickets WHERE channel_id = %s", 
                        (
                            data['channel_id'],
                        )
                    )
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error in TicketDatabase.get: {e}")
            return None
    
    @staticmethod
    def update(data={
        'channel_id': None,
        'claimed': None,
        'claimed_by': None
    }):
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "UPDATE tickets SET claimed = %s, claimed_by = %s WHERE channel_id = %s",
                        (
                            data['claimed'],
                            data['claimed_by'],
                            data['channel_id']
                        )
                    )
                    conn.commit()
        except Exception as e:
            print(f"Error in TicketDatabase.update: {e}")
            return None

    @staticmethod
    def categorys():
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT label, value, description, emote, role_access, channel_category FROM categorys")
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error in TicketDatabase.categorys: {e}")
            return None
        
    @staticmethod
    def category(data={
        'value': None
    }):
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT * FROM categorys WHERE value = %s",
                        (
                            data['value'],
                        ) 
                    )
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error in TicketDatabase.category: {e}")
            return None
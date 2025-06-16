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
    def update(query: str, update_fields: dict):
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    ticket = TicketDatabase.get({'channel_id': query})

                    if not ticket:
                        print("Ticket not found for update.")
                        return None

                    update_set = ', '.join(f"{key} = %s" for key in update_fields.keys())
                    query_values = tuple(update_fields.values()) + (query,)
                    cursor.execute(
                        f"UPDATE tickets SET {update_set} WHERE channel_id = %s",
                        query_values
                    )
                    conn.commit()
                    return TicketDatabase.get({'channel_id': query})
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
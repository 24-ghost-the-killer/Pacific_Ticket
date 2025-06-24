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
        except Database.IntegrityError as e:
            print(f"Integrity error in TicketDatabase.create: {e}")
            return None
        except Database.OperationalError as e:
            print(f"Operational error in TicketDatabase.create: {e}")
            return None
        except Database.DatabaseError as e:
            print(f"Database error in TicketDatabase.create: {e}")
            return None
        except Exception as e:
            print(f"Error in TicketDatabase.create: {e}")
            return None
        
    @staticmethod
    def statistics():
        try:
            with Database.connect() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT COUNT(*) as opened FROM tickets WHERE open = %s", ("1",))
                    opened = cursor.fetchone()["opened"]
                    cursor.execute("SELECT COUNT(*) as total FROM tickets")
                    total = cursor.fetchone()["total"]
                    return {
                        'total': total,
                        'opened': opened
                    }
        except Database.IntegrityError as e:
            print(f"Integrity error in TicketDatabase.statistics: {e}")
            return None
        except Database.OperationalError as e:
            print(f"Operational error in TicketDatabase.statistics: {e}")
            return None
        except Database.DatabaseError as e:
            print(f"Database error in TicketDatabase.statistics: {e}")
            return None
        except Exception as e:
            print(f"Error in TicketDatabase.statistics: {e}")
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
        except Database.IntegrityError as e:
            print(f"Integrity error in TicketDatabase.get: {e}")
            return None
        except Database.OperationalError as e:
            print(f"Operational error in TicketDatabase.get: {e}")
            return None
        except Database.DatabaseError as e:
            print(f"Database error in TicketDatabase.get: {e}")
            return None
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
        except Database.IntegrityError as e:
            print(f"Integrity error in TicketDatabase.update: {e}")
            return None
        except Database.OperationalError as e:
            print(f"Operational error in TicketDatabase.update: {e}")
            return None
        except Database.DatabaseError as e:
            print(f"Database error in TicketDatabase.update: {e}")
            return None 
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
        except Database.IntegrityError as e:
            print(f"Integrity error in TicketDatabase.categorys: {e}")
            return None
        except Database.OperationalError as e:
            print(f"Operational error in TicketDatabase.categorys: {e}")
            return None
        except Database.DatabaseError as e:
            print(f"Database error in TicketDatabase.categorys: {e}")
            return None
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
        except Database.IntegrityError as e:
            print(f"Integrity error in TicketDatabase.category: {e}")
            return None
        except Database.OperationalError as e:
            print(f"Operational error in TicketDatabase.category: {e}")
            return None
        except Database.DatabaseError as e:
            print(f"Database error in TicketDatabase.category: {e}")
            return None
        except Exception as e:
            print(f"Error in TicketDatabase.category: {e}")
            return None
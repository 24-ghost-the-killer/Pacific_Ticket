
class Permission():
    def __init__(self, user, id):
        self.user = user
        self.id = id

    def check(self):
        try:
            return any(
                str(role.id) == str(self.id) 
                for role in getattr(self.user, "roles", [])
            )
        except AttributeError:
            print("User does not have roles attribute.")
            return False
        except TypeError:
            print("Invalid type for user roles or id.")
            return False
        except Exception as e:
            print(f"Error checking permissions: {e}")
            return False
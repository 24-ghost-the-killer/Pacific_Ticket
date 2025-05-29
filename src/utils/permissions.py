class Permission():
    def __init__(self, user, id):
        self.user = user
        self.id = id

    def check(self):
        return any(str(role.id) == str(self.id) for role in getattr(self.user, "roles", []))
class UserRepository:
    def __init__(self):
        self.fake_users_db = {
            "admin@gmail.com": {
                "email": "admin@gmail.com",
                "password": "admin",
            }
        }

    def authenticate_user(self, email: str, password: str) -> bool:
        user = self.fake_users_db.get(email)
        if user and user["password"] == password:
            return True
        return False

class SessionManager:
    def __init__(self):
        self.token = None

    def login(username: str, password: str, token: str):
        pass

    def logout(self):
        self.token = None

    def is_autenticated(self):
        return self.token is not None

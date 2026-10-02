from token import Token

from data_manager import DataManager


class Manager:
    def __init__(
        self,
        firstname: str,
        lastname: str,
        username: str,
        password: str,
        national_code: str,
    ):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.code = national_code

    @classmethod
    def get_manager_as_dict(cls, id: int):
        return DataManager.get_object(id, Manager)

    @classmethod
    def is_exists(cls, national_code):
        return DataManager.is_exists_by_code(national_code)

    @staticmethod
    def login(username: str, password: str):
        managers = DataManager.get_data(Manager.__name__ + ".json")
        for m in managers:
            if m["username"] == username and m["password"] == password:
                t = Token.build_and_save_Token(m["code"], Manager)
                print("token created")
                return t

        print("username or password is wrong")
        return None

from data_manager import DataManager


class User:
    def __init__(self, username: str, password: str, national_code: str, type: str):
        self.username = username
        self.password = password
        self.code = national_code
        self.type = type
        User.add_user(national_code,username,password,type)
    @staticmethod
    def add_user(national_code,username,password,type):
        DataManager.registeration({"code":national_code,"username":username,"password":password,"type":type},"User.json")
    

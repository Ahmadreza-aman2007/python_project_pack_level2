import json
from pathlib import Path


class DataManager:
    database_directory = Path("data")

    @staticmethod
    def check_file_exist(file_name: str) -> bool:
        file_path = DataManager.database_directory / file_name
        return file_path.exists()

    @staticmethod
    def create_file(file_name: str):
        DataManager.database_directory.mkdir(exist_ok=True)
        file_path = DataManager.database_directory / file_name
        with file_path.open("w") as file:
            file.write("[]")

    @staticmethod
    def get_data(database: str) -> list:
        file_path = DataManager.database_directory / database
        with file_path.open() as file:
            return json.load(file)

    @staticmethod
    def check_object_exists(obj, database_list: list) -> bool:
        for element in database_list:
            if obj.code == element["code"]:
                return True
        return False

    @staticmethod
    def obj_to_dict(obj: object) -> dict:
        d = vars(obj)
        d["d_id"] = DataManager.get_last_id(obj.__class__.__name__ + ".json")
        return d

    @staticmethod
    def get_last_id(database: str) -> int:
        database_list = DataManager.get_data(database)
        if not database_list:
            return 1
        return max(item["d_id"] for item in database_list) + 1

    @staticmethod
    def get_object(id: int, cls) -> dict:

        for i in DataManager.get_data(cls.__name__ + ".json"):
            if i["id"] == id:
                return i
        return None

    def save(self, cls, databaselist: list):
        file_name = cls.__name__ + ".json"
        with open(DataManager.database_directory / file_name, "w") as file:
            json.dump(databaselist, file)

    def add(self, obj: object):
        database = obj.__class__.__name__ + ".json"
        if not DataManager.check_file_exist(database):
            DataManager.create_file(database)
        if DataManager.check_object_exists(obj, self.get_data(database=database)):
            raise AlreadyExistsError(f"{obj.__class__.__name__} alredy exists")
        database_list = DataManager.get_data(obj.__class__.__name__ + ".json")
        database_list.append(DataManager.obj_to_dict(obj=obj))
        self.save(obj.__class__, database_list)


class AlreadyExistsError(Exception):
    pass


class Student:
    def __init__(
        self,
        firstname: str,
        lastname: str,
        major_id: int,
        national_code: str,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.major_id = major_id
        self.code = national_code

    @classmethod
    def get_student(cls, id: int) -> dict:
        return DataManager.get_object(id, Student)


class Teacher:
    def __init__(
        self,
        firstname: str,
        lastname: str,
        specialized_lesson_id: int,
        national_code: str,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.specialized_lesson = specialized_lesson_id
        self.code = national_code

    @classmethod
    def get_teacher(cls, id: int) -> dict:
        return DataManager.get_object(id, Teacher)


class Lesson:
    def __init__(self, name: str, lesson_code: int):
        self.name = name
        self.code = lesson_code

    @classmethod
    def get_lesson(cls, id: int):
        return DataManager.get_object(id, Lesson)


class Major:
    def __init__(self, name: str, major_code: str):
        self.name = name
        self.code = major_code

    @classmethod
    def get_major(cls, id: int):
        return DataManager.get_object(id, Major)


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
    def get_manager(cls, id: int):
        return DataManager.get_object(id, Manager)


datamanager: DataManager = DataManager()
datamanager.add(Student(1, "agijaerk", "dsalgio;", "aosdigjkdil", "dsig"))

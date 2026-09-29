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
        d["id"] = DataManager.get_last_id(obj.__class__.__name__ + ".json")
        return d

    @staticmethod
    def get_last_id(database: str) -> int:
        database_list = DataManager.get_data(database)
        if not database_list:
            return 1
        return max(item["id"] for item in database_list) + 1

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

    def registeration(self, obj: object):
        database = obj.__class__.__name__ + ".json"
        if not DataManager.check_file_exist(database):
            DataManager.create_file(database)
        if DataManager.check_object_exists(obj, self.get_data(database=database)):
            raise AlreadyExistsError(f"{obj.__class__.__name__} alredy exists")
        database_list = DataManager.get_data(obj.__class__.__name__ + ".json")
        database_list.append(DataManager.obj_to_dict(obj=obj))
        self.save(obj.__class__, database_list)

    def update(self, obj: object):
        database = obj.__class__.__name__ + ".json"
        if not DataManager.check_file_exist(database):
            raise FileNotFoundError("database dosent exist.")
        if not DataManager.check_object_exists(
            obj=obj, database_list=self.get_data(database)
        ):
            raise ObjectDosentExistError(f"{obj.__class__.__name__} dosen't exist")
        database_list = DataManager.get_data(database=database)
        for index, element in enumerate(database_list):
            if element["code"] == obj.code:
                object_id = element["id"]
                database_list[index] = DataManager.obj_to_dict(obj)
                database_list[index]["id"] = object_id
                self.save(obj.__class__, database_list)
                break


class AlreadyExistsError(Exception):
    pass


class ObjectDosentExistError(Exception):
    pass


class Major:
    def __init__(self, name: str, major_code: str):
        self.name = name
        self.code = major_code

    @classmethod
    def get_major(cls, id: int) -> dict:
        return DataManager.get_object(id, Major)

    @classmethod
    def dict_to_major(d: dict) -> "Major":
        if not d or not d["name"] or not d["code"]:
            return None
        return Major(d["name"], d["code"])


class Lesson:
    def __init__(self, name: str, lesson_code: int):
        self.name = name
        self.code = lesson_code

    @classmethod
    def get_lesson(cls, id: int):
        return DataManager.get_object(id, Lesson)

    @classmethod
    def dict_to_lesson(d: dict) -> "Lesson":
        if not d or not d["name"] or not d["code"]:
            return None
        return Lesson(d["name"], d["code"])


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
    def get_student_as_dict(cls, id: int) -> dict:
        return DataManager.get_object(id, Student)

    def get_major(self) -> Major:
        return Major.dict_to_major(Major.get_major(self.major_id))


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
    def get_teacher_as_dict(cls, id: int) -> dict:
        return DataManager.get_object(id, Teacher)

    def get_lesson(self):
        return Lesson.dict_to_lesson(Lesson.get_lesson(self.specialized_lesson))


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


datamanager: DataManager = DataManager()

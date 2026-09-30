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
        if not file_path.exists():
            DataManager.create_file(database)
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

    @staticmethod
    def is_exists_by_code(code: int | str, cls: object):
        datas = DataManager.get_data(cls.__name__ + ".json")
        for i in datas:
            if i["code"] == code:
                return True
        return False

    @staticmethod
    def save(clas, databaselist: list):
        file_name = clas.__name__ + ".json"
        with open(DataManager.database_directory / file_name, "w") as file:
            json.dump(databaselist, file, indent=4)

    @staticmethod
    def registeration(obj: object):
        database = obj.__class__.__name__ + ".json"
        if not DataManager.check_file_exist(database):
            DataManager.create_file(database)
        if DataManager.check_object_exists(
            obj, DataManager.get_data(database=database)
        ):
            raise AlreadyExistsError(f"{obj.__class__.__name__} alredy exists")
        database_list = DataManager.get_data(obj.__class__.__name__ + ".json")
        database_list.append(DataManager.obj_to_dict(obj=obj))
        if obj.__class__ == Student:
            DataManager.registeration(Student_lessons(obj.code, []))
        DataManager.save(obj.__class__, database_list)

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

    def delete(self, obj: object):
        database = obj.__class__.__name__ + ".json"
        if not DataManager.check_file_exist(database):
            raise FileNotFoundError("database dosent exist.")
        if not DataManager.check_object_exists(
            obj=obj, database_list=self.get_data(database)
        ):
            raise ObjectDosentExistError(f"{obj.__class__.__name__} dosen't exist")
        database_list = DataManager.get_data(database=database)
        for element in database_list:
            if element["code"] == obj.code:
                database_list.remove(element)
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

    @classmethod
    def is_exists(cls, code: int | str):
        return DataManager.is_exists_by_code(code, Major)


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


class Student_lessons:
    def __init__(self, student_code: str, lessons: list[int]):
        self.code = student_code
        self.lessons = lessons


import datetime
import secrets


class Token:
    live_time_for_tokens = 1

    def __init__(
        self,
        token: str,
        created_at: datetime.datetime,
        expired_at: datetime.datetime,
        owner_code: str | int,
        object_type: str,
    ):
        self.token = token
        self.created_at = created_at
        self.expired_at = expired_at
        self.owner_code = owner_code
        self.is_active = True
        self.object_type = object_type

    @staticmethod
    def build_and_save_Token(personal_code: int | str, cls: object) -> str:
        token = secrets.token_urlsafe()
        created_at = datetime.datetime.now().isoformat()
        expired_at = (
            datetime.datetime.fromisoformat(created_at)
            + datetime.timedelta(seconds=Token.live_time_for_tokens)
        ).isoformat()
        Token.save_token(
            Token(token, created_at, expired_at, personal_code, cls.__name__)
        )
        return token

    @staticmethod
    def get_tokens() -> list:
        directory_path = DataManager.database_directory
        database_path = directory_path / "token.json"
        if not directory_path.exists():
            directory_path.mkdir()
        if not database_path.exists():
            return []
        with database_path.open("r") as file:
            return json.load(file)

    @staticmethod
    def save_token(token: "Token"):
        print(vars(token))
        tokens = Token.get_tokens()
        tokens.append(vars(token))
        print(tokens)
        with (DataManager.database_directory / "token.json").open("w") as file:
            json.dump(tokens, file, indent=4)

    @staticmethod
    def update_tokens(token: "Token"):
        tokens = Token.get_tokens()
        for t in tokens:
            if t["token"] == token.token:
                tokens.remove(t)
                tokens.append(vars(token))
                break
        with (DataManager.database_directory / "token.json").open("w") as file:
            json.dump(tokens, file, indent=4)

    @staticmethod
    def expire_token(token: "Token"):
        token.is_active = False
        Token.update_tokens(token=token)

    @staticmethod
    def delete(token: str):
        tokens = Token.get_tokens()
        for t in tokens:
            if t["token"] == token:
                tokens.remove(t)
        with (DataManager.database_directory / "token.json").open("w") as file:
            json.dump(tokens, file, indent=4)

    @staticmethod
    def token_vrification(token: str, personal_code: int | str, cls: str):
        tokens = Token.get_tokens()
        for t in tokens:
            if (
                t["owner_code"] == personal_code
                and t["object_type"] == cls
                and t["token"] == token
            ):
                if (
                    datetime.datetime.fromisoformat(t["expired_at"])
                    < datetime.datetime.now()
                    or not t["is_active"]
                ):
                    print("your token is expired")
                    Token.delete(token=token)
                    return
                else:
                    return True

        print("token not found")
        return False


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

    def get_lessons(self) -> list:
        all_lessons = DataManager.get_data("Student_lessons.json")
        for element in all_lessons:
            if self.code == element["code"]:
                return element["lessons"]
        return None

    def add_new_lesson(self, lesson_code: int):
        all_lessons = DataManager.get_data("Student_lessons.json")
        lessons = None
        for element in all_lessons:
            if self.code == element["code"]:
                lessons = element["lessons"]
                break
        if lessons == None:
            raise ObjectDosentExistError("can not find student's lessons")
        if lesson_code in lessons:
            print("you have this lesson")
            return
        lessons.append(lesson_code)
        d = DataManager()
        d.save(lesson_code, all_lessons)

    @staticmethod
    def is_exists(national_code: str) -> bool:
        return DataManager.is_exists_by_code(national_code, Student)


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


manager: Manager = Manager("admin", "admin", "admin", "admin", 2)
Token.token_vrification(
    "wzXWsH3oapUV88YebeHYdD4v5mITVySnw_VmSmgXQPI", 2, Manager.__name__
)

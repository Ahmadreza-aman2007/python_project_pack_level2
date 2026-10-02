from student_lessons import Student_lessons


class DataManager:
    from pathlib import Path

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
        from json import load
        file_path = DataManager.database_directory / database
        if not file_path.exists():
            DataManager.create_file(database)
        with file_path.open() as file:
            return load(file)

    @staticmethod
    def check_object_exists(obj_code: str | int, database_name: str) -> bool:
        database_list = DataManager.get_data(database_name)
        if not database_list:
            print(f"{database_name} database is empty")
        for element in database_list:
            if obj_code == element["code"]:
                return True
        return False

    @staticmethod
    def obj_to_dict(obj: object) -> dict:
        d = vars(obj)
        return d

    @staticmethod
    def get_last_id(database: str) -> int:
        database_list = DataManager.get_data(database)
        if not database_list:
            return 1
        return max(item["id"] for item in database_list) + 1

    @staticmethod
    def get_object_by_id(id: int, database_name: str) -> dict:

        for i in DataManager.get_data(database_name):
            if i["id"] == id:
                return i
        return None

    @staticmethod
    def get_object_by_code(code: str | int, database_name: str) -> dict:
        for i in DataManager.get_data(database_name):
            if i["code"] == id:
                return i
        return None


    @staticmethod
    def is_exists_by_code(code: int | str,database_name:str):
        datas = DataManager.get_data(database_name)
        for i in datas:
            if i["code"] == code:
                return True
        return False

    @staticmethod
    def save(database_name, databaselist: list):
        from json import dump
        with open(DataManager.database_directory / database_name, "w") as file:
            dump(databaselist, file, indent=4)

    @staticmethod
    def registeration(json_data:dict,database_name:str):
        if not DataManager.check_file_exist(database_name):
            DataManager.create_file(database_name)
        if DataManager.check_object_exists(
            json_data["code"], database_name
        ):
            from exceptions import AlreadyExistsError
            raise AlreadyExistsError(f"{database_name.split(".")[0]}object already exists")
        database_list = DataManager.get_data(database_name)
        json_data["id"] = DataManager.get_last_id(database_name)

        database_list.append(json_data)
        if database_name == "Student.json":
            DataManager.registeration(Student_lessons(json_data["code"], []))
        DataManager.save(database_name, database_list)

    @staticmethod
    def update(obj: object):
        database = obj.__class__.__name__ + ".json"
        if not DataManager.check_file_exist(database):
            raise FileNotFoundError("database dosent exist.")
        if not DataManager.check_object_exists(
            obj=obj, database_list=DataManager.get_data(database)
        ):
            from exceptions import ObjectDosentExistError

            raise ObjectDosentExistError(f"{obj.__class__.__name__} dosen't exist")
        database_list = DataManager.get_data(database=database)
        for index, element in enumerate(database_list):
            if element["code"] == obj.code:
                object_id = element["id"]
                database_list[index] = DataManager.obj_to_dict(obj)
                database_list[index]["id"] = object_id
                DataManager.save(obj.__class__, database_list)
                break

    @staticmethod
    def delete(obj: object):
        database = obj.__class__.__name__ + ".json"
        if not DataManager.check_file_exist(database):
            raise FileNotFoundError("database dosent exist.")
        if not DataManager.check_object_exists(
            obj=obj, database_list=DataManager.get_data(database)
        ):
            from exceptions import ObjectDosentExistError

            raise ObjectDosentExistError(f"{obj.__class__.__name__} dosen't exist")
        database_list = DataManager.get_data(database=database)
        for element in database_list:
            if element["code"] == obj.code:
                database_list.remove(element)
                DataManager.save(obj.__class__, database_list)
                break

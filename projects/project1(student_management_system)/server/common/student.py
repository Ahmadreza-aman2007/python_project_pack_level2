from data_manager import DataManager
from exceptions import ObjectDosentExistError
from major import Major
from user import User


class Student(User):
    def __init__(
        self,
        username:str,
        password:str,
        firstname: str,
        lastname: str,
        major_id: int,
        national_code: str,
    ):
        super().__init__(username,password,national_code,"Student")
        self.firstname = firstname
        self.lastname = lastname
        self.major_id = major_id

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

from data_manager import DataManager
from lessons import Lesson


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

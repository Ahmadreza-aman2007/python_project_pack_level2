from data_manager import DataManager


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

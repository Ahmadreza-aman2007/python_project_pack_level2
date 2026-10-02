from data_manager import DataManager


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

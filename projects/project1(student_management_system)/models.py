from pathlib import Path
import json
import os
from typing import Any, Dict, List, Optional


class DataManager:
    """Handles file system interactions for JSON data storage."""

    _CURRENT_FILE_PATH: Path = Path(__file__).resolve()
    _PROJECT_ROOT: Path = _CURRENT_FILE_PATH.parent
    _DB_DIR: Path = _PROJECT_ROOT / "database"

    @staticmethod
    def get_db_path(filename: str) -> str:
        """Returns the absolute path to a file inside the database directory."""
        return str(DataManager._DB_DIR / filename)

    @staticmethod
    def load_json(filename: str) -> Dict[str, Any]:
        """Loads data from a JSON file and returns it as a dictionary."""
        file_path: str = DataManager.get_db_path(filename)
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data: Dict[str, Any] = json.load(file)
                return data
        except Exception:
            return {}

    @staticmethod
    def save_json(filename: str, data: Dict[str, Any]) -> None:
        """Saves a dictionary to a JSON file."""
        file_path: str = DataManager.get_db_path(filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class Major:
    """Represents an academic major."""

    def __init__(self, major_id: int, name: str) -> None:
        """Initializes a new major."""
        self.id: int = major_id
        self.name: str = name

    def to_dict(self) -> Dict[str, Any]:
        """Converts object attributes to a dictionary."""
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Major":
        """Creates a Major instance from a dictionary."""
        return cls(data["id"], data["name"])

    @classmethod
    def get_all_as_list(cls) -> List["Major"]:
        """Retrieves all majors from the database as a list of Major objects."""
        raw_data: Dict[str, Any] = DataManager.load_json("majors.json")
        return [cls.from_dict(m) for m in raw_data.values()]

    @classmethod
    def save_majors(cls, majors: List["Major"]) -> None:
        """Saves a list of Major objects to the database."""
        data_to_save: Dict[str, Any] = {str(m.id): m.to_dict() for m in majors}
        DataManager.save_json("majors.json", data_to_save)

    @staticmethod
    def get_major_by_id(major_id: int) -> Optional["Major"]:
        """Finds a specific major by its ID. Returns None if not found."""
        majors: List["Major"] = Major.get_all_as_list()
        return next((m for m in majors if m.id == major_id), None)


class Lesson:
    """Represents an individual lesson/course within a major."""

    def __init__(self, lesson_id: int, name: str, major: Major) -> None:
        """Initializes a new lesson.

        Args:
            lesson_id: Unique identifier for the lesson.
            name: Name of the lesson.
            major: A Major object that this lesson belongs to.
        """
        self.id: int = lesson_id
        self.name: str = name
        self.major: Major = major

    def to_dict(self) -> Dict[str, Any]:
        """Converts lesson attributes to a dictionary for JSON serialization.
        Note: Only stores the major_id, not the full Major object.
        """
        return {"id": self.id, "name": self.name, "major_id": self.major.id}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Lesson":
        """Creates a Lesson instance from a dictionary.
        Note: Uses Major.get_major_by_id to reconstruct the Major object.
        """
        major_obj: Optional[Major] = Major.get_major_by_id(data["major_id"])
        if major_obj is None:
            raise ValueError(f"Major with id {data['major_id']} not found.")

        return cls(data["id"], data["name"], major_obj)

    @classmethod
    def get_all_as_list(cls) -> List["Lesson"]:
        """Retrieves all lessons from the database as a list of Lesson objects."""
        raw_data: Dict[str, Any] = DataManager.load_json("lessons.json")
        return [cls.from_dict(l) for l in raw_data.values()]

    @classmethod
    def save_lessons(cls, lessons: List["Lesson"]) -> None:
        """Saves a list of lesson objects to the database."""
        data_to_save: Dict[str, Any] = {str(l.id): l.to_dict() for l in lessons}
        DataManager.save_json("lessons.json", data_to_save)

    @staticmethod
    def get_lesson_by_id(lesson_id: int) -> Optional["Lesson"]:
        """Finds a specific lesson by its ID. Returns None if not found."""
        lessons: List["Lesson"] = Lesson.get_all_as_list()
        return next((l for l in lessons if l.id == lesson_id), None)


class Course:
    """Represents an academic class/group (renamed from 'Class' for clarity)."""

    def __init__(self, course_id: int, name: str) -> None:
        """Initializes a new course/group.

        Args:
            course_id: Unique identifier for the course.
            name: Name of the course (e.g., 'Group A', 'Semester 1').
        """
        self.id: int = course_id
        self.name: str = name

    def to_dict(self) -> Dict[str, Any]:
        """Converts course attributes to a dictionary."""
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Course":
        """Creates a Course instance from a dictionary."""
        return cls(data["id"], data["name"])

    @classmethod
    def get_all_as_list(cls) -> List["Course"]:
        """Retrieves all courses from the database as a list of Course objects."""
        raw_data: Dict[str, Any] = DataManager.load_json("courses.json")
        return [cls.from_dict(c) for c in raw_data.values()]

    @classmethod
    def save_courses(cls, courses: List["Course"]) -> None:
        """Saves a list of course objects to the database."""
        data_to_save: Dict[str, Any] = {str(c.id): c.to_dict() for c in courses}
        DataManager.save_json("courses.json", data_to_save)

    @staticmethod
    def get_course_by_id(course_id: int) -> Optional["Course"]:
        """Finds a specific course by its ID. Returns None if not found."""
        courses: List["Course"] = Course.get_all_as_list()
        return next((c for c in courses if c.id == course_id), None)


class Student:
    """Represents a student within the management system."""

    def __init__(self, student_id: int, name: str, major: Major) -> None:
        """Initializes a new student.

        Args:
            student_id: Unique identifier for the student.
            name: Full name of the student.
            major: A Major object that this student belongs to.
        """
        self.id: int = student_id
        self.name: str = name
        self.major: Major = major
        self.enrolled_lessons: List[Lesson] = []

    def enroll_in_lesson(self, lesson: Lesson) -> None:
        """Enrolls the student in a specific lesson.

        Args:
            lesson: The Lesson object to be added.
        """
        if lesson not in self.enrolled_lessons:
            self.enrolled_lessons.append(lesson)

    def to_dict(self) -> Dict[str, Any]:
        """Converts student attributes to a dictionary for JSON serialization.
        Stores major_id and a list of lesson_ids.
        """
        return {
            "id": self.id,
            "name": self.name,
            "major_id": self.major.id,
            "lesson_ids": [lesson.id for lesson in self.enrolled_lessons],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Creates a Student instance from a dictionary and reconstructs objects.

        Args:
            data: The dictionary containing student data.

        Returns:
            A fully reconstructed Student object.
        """
        major_obj: Optional[Major] = Major.get_major_by_id(data["major_id"])
        if major_obj is None:
            raise ValueError(f"Major with id {data['major_id']} not found.")
        student = cls(data["id"], data["name"], major_obj)
        lesson_ids: List[int] = data.get("lesson_ids", [])
        for l_id in lesson_ids:
            lesson_obj: Optional[Lesson] = Lesson.get_lesson_by_id(l_id)
            if lesson_obj:
                student.enroll_in_lesson(lesson_obj)
            else:
                print(
                    f"Warning: Lesson with id {l_id} not found for student {student.id}"
                )

        return student

    @classmethod
    def get_all_as_list(cls) -> List["Student"]:
        """Retrieves all students from the database."""
        raw_data: Dict[str, Any] = DataManager.load_json("students.json")
        return [cls.from_dict(s) for s in raw_data.values()]

    @classmethod
    def save_students(cls, students: List["Student"]) -> None:
        """Saves a list of student objects to the database."""
        data_to_save: Dict[str, Any] = {str(s.id): s.to_dict() for s in students}
        DataManager.save_json("students.json", data_to_save)

    @staticmethod
    def get_student_by_id(student_id: int) -> Optional["Student"]:
        """Finds a specific student by their ID."""
        students: List["Student"] = Student.get_all_as_list()
        return next((s for s in students if s.id == student_id), None)


class Teacher:
    """Represents a teacher specialized in a specific lesson."""

    def __init__(
        self,
        teacher_id: int,
        firstname: str,
        lastname: str,
        specialized_lesson: "Lesson",
    ) -> None:
        """Initialize a Teacher object.

        Args:
            teacher_id: Unique identifier for the teacher.
            firstname: First name of the teacher.
            lastname: Last name of the teacher.
            specialized_lesson: The Lesson object the teacher specializes in.
        """
        self.id: int = teacher_id
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.specialized_lesson: "Lesson" = specialized_lesson

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Teacher object to a dictionary for storage.

        Returns:
            A dictionary with teacher details and their lesson ID.
        """
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "lesson_id": self.specialized_lesson.id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Teacher":
        """Create a Teacher instance from a dictionary.

        Args:
            data: A dictionary containing teacher attributes.

        Returns:
            A reconstructed Teacher object.
        """
        lesson_obj = Lesson.get_lesson_by_id(
            Lesson.get_all_as_list(), data["lesson_id"]
        )

        return cls(
            data["id"],
            data["firstname"],
            data["lastname"],
            lesson_obj,
        )

    @classmethod
    def get_all_as_list(cls) -> List["Teacher"]:
        """Retrieve all teachers from the database as a list of objects.

        Returns:
            A list of all Teacher instances.
        """
        raw_data: Dict[str, Any] = DataManager.load_json("teachers.json")
        return [cls.from_dict(m) for m in raw_data.values()]

    @classmethod
    def save_teachers(cls, teachers: List["Teacher"]) -> None:
        """Save a list of Teacher objects to the JSON file.

        Args:
            teachers: The list of teachers to save.
        """
        data_to_save: Dict[int, Dict[str, Any]] = {}
        for teacher in teachers:
            data_to_save[teacher.id] = teacher.to_dict()

        DataManager.save_json("teachers.json", data_to_save)

    @classmethod
    def get_teachers(cls) -> Dict[str, Any]:
        """Load and return the raw teachers data from the JSON file.

        Returns:
            A dictionary containing the raw data of teachers.
        """
        return DataManager.load_json("teachers.json")


class Manager:
    """Represents a manager in the student management system."""

    def __init__(
        self,
        manager_id: int,
        firstname: str,
        lastname: str,
        username: str,
        password: str,
    ) -> None:
        """Initialize a Manager object.

        Args:
            manager_id: Unique identifier of the manager.
            firstname: First name of the manager.
            lastname: Last name of the manager.
            username: Username used for authentication.
            password: Password used for authentication.
        """
        self.id: int = manager_id
        self.username: str = username
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.password: str = password

    @classmethod
    def get_managers(cls) -> Dict[str, Any]:
        """Load and return the raw managers data from the JSON file.

        Returns:
            A dictionary containing the managers' raw data.
        """
        return DataManager.load_json("managers.json")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Manager object to a dictionary.

        Returns:
            A dictionary containing the manager's attributes.
        """
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Manager":
        """Create a Manager object from a dictionary.

        Args:
            data: A dictionary containing manager information.

        Returns:
            A new Manager instance created from the provided data.
        """
        return cls(
            data["id"],
            data["firstname"],
            data["lastname"],
            data["username"],
            data["password"],
        )

    @classmethod
    def get_all_as_list(cls) -> List["Manager"]:
        """Load all managers and return them as a list of objects.

        Returns:
            A list containing all Manager instances.
        """
        raw_data: Dict[str, Any] = DataManager.load_json("managers.json")
        return [cls.from_dict(m) for m in raw_data.values()]

    @classmethod
    def save_managers(cls, managers: List["Manager"]) -> None:
        """Save a list of managers to the JSON file.

        Args:
            managers: A list of Manager objects to be saved.
        """
        data_to_save: Dict[int, Dict[str, Any]] = {}

        for manager in managers:
            data_to_save[manager.id] = manager.to_dict()

        DataManager.save_json("managers.json", data_to_save)

class Student:
    def __init__(self, student_id, firstname, lastname, major):
        self.id = student_id
        self.firstname = firstname
        self.lastname = lastname
        self.major = major


class Teacher:
    def __init__(self, teacher_id, firstname, lastname, specialized_lesson):
        self.firstname = firstname
        self.lastname = lastname
        self.specialized_lesson = specialized_lesson
        self.id = teacher_id


class Lesson:
    def __init__(self, lesson_id, name):
        self.id = lesson_id
        self.name = name


class Major:
    def __init__(self, major_id, name):
        self.id = major_id
        self.name = name


class Manager:
    def __init__(self, manager_id, firstname, lastname, username, password):
        self.id = manager_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

"""Student records."""


class Student:
    def __init__(self, student_id: str, name: str, **details: str) -> None:
        self._id = student_id
        self.name = name  # validated by the setter
        self._details = details

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def details(self) -> dict[str, str]:
        return dict(self._details)  # copy, so callers can't change it directly

    @property
    def level(self) -> str:
        return "Student"


class UndergraduateStudent(Student):
    @property
    def level(self) -> str:
        return "Undergraduate"


class GraduateStudent(Student):
    @property
    def level(self) -> str:
        return "Graduate"


# List stores the collection, dictionary maps IDs to students
students: list[Student] = []
students_by_id: dict[str, Student] = {}


def add_student(name: str, student_type: type[Student] = UndergraduateStudent, **details: str) -> Student:
    """Register a new student and return it.

    Any extra keyword arguments (e.g. email="...") are stored on the student.
    """
    student = student_type(f"S{len(students) + 1:03d}", name, **details)
    students.append(student)
    students_by_id[student.id] = student
    return student


def get_student(student_id: str) -> Student | None:
    return students_by_id.get(student_id.upper())

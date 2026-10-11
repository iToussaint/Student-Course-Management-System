"""Student records."""

from typing import Self


class Student:
    _count = 0  # shared by all student types, used to number new IDs

    def __init__(self, student_id: str, name: str, **details: str) -> None:
        self._id = student_id
        self.name = name  # validated by the setter
        self._details = details

    @classmethod
    def create(cls, name: str, **details: str) -> Self:
        """Create a student of this class with the next available ID."""
        Student._count += 1
        return cls(f"S{Student._count:03d}", name, **details)

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

    def __repr__(self) -> str:
        # type(self) gives the subclass name, e.g. GraduateStudent(...)
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


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
    student = student_type.create(name, **details)
    students.append(student)
    students_by_id[student.id] = student
    return student


def get_student(student_id: str) -> Student | None:
    return students_by_id.get(student_id.upper())

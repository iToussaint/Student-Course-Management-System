"""Student records: the student class hierarchy and the student registry."""

from abc import ABC, abstractmethod
from typing import Self


class Student(ABC):
    """A registered student.

    Student is abstract: each student type must say which level it is,
    so only the concrete subclasses can be created.

    Args:
        student_id: Unique ID such as "S001".
        name: Full name; must not be empty.
        **details: Optional extra information, e.g. email="...".
    """

    def __init__(self, student_id: str, name: str, **details: str) -> None:
        self._id = student_id
        self.name = name  # validated by the setter
        self._details = details

    @classmethod
    def register(cls, name: str, **details: str) -> Self:
        """Create a student of this class, store it, and return it.

        Called on a subclass (e.g. GraduateStudent.register) it creates
        that subclass. IDs come from the registry size, so every ID
        belongs to a stored student and there are no gaps.
        """
        student = cls(f"S{len(students) + 1:03d}", name, **details)
        students.append(student)
        students_by_id[student.id] = student
        return student

    @property
    def id(self) -> str:
        """The student's ID (read-only)."""
        return self._id

    @property
    def name(self) -> str:
        """The student's full name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def details(self) -> dict[str, str]:
        """Extra details, returned as a copy so they can't be changed."""
        return dict(self._details)

    @property
    @abstractmethod
    def level(self) -> str:
        """Study level shown in reports, e.g. "Graduate"."""

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
    """A student working towards a first degree."""

    @property
    def level(self) -> str:
        """Study level shown in reports."""
        return "Undergraduate"


class GraduateStudent(Student):
    """A student working towards a postgraduate degree."""

    @property
    def level(self) -> str:
        """Study level shown in reports."""
        return "Graduate"


# List stores the collection, dictionary maps IDs to students
students: list[Student] = []
students_by_id: dict[str, Student] = {}


def add_student(
    name: str,
    student_type: type[Student] = UndergraduateStudent,
    **details: str,
) -> Student:
    """Register a new student of the given type and return it.

    Args:
        name: The student's full name.
        student_type: Which Student subclass to create.
        **details: Optional extra information, e.g. email="...".
    """
    return student_type.register(name, **details)


def get_student(student_id: str) -> Student | None:
    """Return the student with this ID (case-insensitive), or None."""
    return students_by_id.get(student_id.upper())

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
    def create(cls, number: int, name: str, **details: str) -> Self:
        """Create a student of this class from a sequence number.

        Called on a subclass (e.g. GraduateStudent.create) it creates
        that subclass. The number is turned into an ID such as "S001".
        """
        return cls(f"S{number:03d}", name, **details)

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


class StudentRegistry:
    """Stores registered students and looks them up by ID."""

    def __init__(self) -> None:
        # List stores the collection, dictionary maps IDs to students
        self._students: list[Student] = []
        self._students_by_id: dict[str, Student] = {}

    def add(
        self,
        name: str,
        student_type: type[Student] = UndergraduateStudent,
        **details: str,
    ) -> Student:
        """Register a new student of the given type and return it.

        IDs come from the registry size, so every ID belongs to a stored
        student and there are no gaps.

        Args:
            name: The student's full name.
            student_type: Which Student subclass to create.
            **details: Optional extra information, e.g. email="...".
        """
        student = student_type.create(len(self._students) + 1, name, **details)
        self._students.append(student)
        self._students_by_id[student.id] = student
        return student

    def get(self, student_id: str) -> Student | None:
        """Return the student with this ID (case-insensitive), or None."""
        return self._students_by_id.get(student_id.upper())

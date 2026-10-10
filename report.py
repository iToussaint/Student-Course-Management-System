"""Report generation."""

from abc import ABC, abstractmethod

from course import Course
from enrollment import get_roster, get_student_enrollments, student_average
from student import Student


def format_grade(grade: float | None) -> str:
    return "-" if grade is None else f"{grade:.1f}"


class Report(ABC):
    """Base class for all reports. Subclasses supply the title and body lines."""

    @property
    @abstractmethod
    def title(self) -> str: ...

    @abstractmethod
    def lines(self) -> list[str]: ...

    def generate(self) -> str:
        return "\n".join([self.title, "-" * len(self.title), *self.lines()])


class StudentSummaryReport(Report):
    def __init__(self, student: Student) -> None:
        self._student = student

    @property
    def title(self) -> str:
        return f"Summary for {self._student.name} ({self._student.id}, {self._student.level})"

    def lines(self) -> list[str]:
        enrolled = get_student_enrollments(self._student)
        return [
            f"Courses enrolled: {len(enrolled)}",
            *[f"  {e.course.code:<8} {e.course.title:<30} Grade: {format_grade(e.grade)}" for e in enrolled],
            f"Average grade: {format_grade(student_average(self._student))}",
        ]


class CourseRosterReport(Report):
    def __init__(self, course: Course) -> None:
        self._course = course

    @property
    def title(self) -> str:
        return f"Roster for {self._course.code} - {self._course.title}"

    def lines(self) -> list[str]:
        roster = get_roster(self._course)
        if not roster:
            return ["No students enrolled."]
        return [f"{len(roster)} student(s)"] + [
            f"  {e.student.id}  {e.student.name:<25} {e.student.level:<14} Grade: {format_grade(e.grade)}"
            for e in roster
        ]

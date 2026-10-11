"""Report generation built on an abstract Report base class."""

from abc import ABC, abstractmethod

from course import Course
from enrollment import get_roster, get_student_enrollments, student_average
from student import Student


class Report(ABC):
    """Base class for all reports.

    Subclasses supply the title and body lines; generate() puts them
    together, so every report is laid out the same way.
    """

    @property
    @abstractmethod
    def title(self) -> str:
        """Heading printed at the top of the report."""

    @abstractmethod
    def lines(self) -> list[str]:
        """Return the body lines of the report."""

    def generate(self) -> str:
        """Return the full report text: title, underline, then body."""
        return "\n".join([self.title, "-" * len(self.title), *self.lines()])

    @staticmethod
    def format_grade(grade: float | None) -> str:
        """Format a grade to one decimal place, or "-" if missing."""
        return "-" if grade is None else f"{grade:.1f}"


class StudentSummaryReport(Report):
    """A student's courses, grades, and average grade."""

    def __init__(self, student: Student) -> None:
        self._student = student

    @property
    def title(self) -> str:
        """Heading with the student's name, ID, and level."""
        student = self._student
        # student.level is polymorphic: each student type supplies its own
        return f"Summary for {student.name} ({student.id}, {student.level})"

    def lines(self) -> list[str]:
        """Return one line per course, followed by the average grade."""
        enrolled = get_student_enrollments(self._student)
        average = student_average(self._student)
        return [
            f"Courses enrolled: {len(enrolled)}",
            *[
                f"  {e.course.code:<8} {e.course.title:<30} "
                f"Grade: {self.format_grade(e.grade)}"
                for e in enrolled
            ],
            f"Average grade: {self.format_grade(average)}",
        ]


class CourseRosterReport(Report):
    """Everyone enrolled in a course, with their level and grade."""

    def __init__(self, course: Course) -> None:
        self._course = course

    @property
    def title(self) -> str:
        """Heading with the course code and title."""
        return f"Roster for {self._course.code} - {self._course.title}"

    def lines(self) -> list[str]:
        """Return a count line, then one line per enrolled student."""
        roster = get_roster(self._course)
        if not roster:
            return ["No students enrolled."]
        return [f"{len(roster)} student(s)"] + [
            f"  {e.student.id}  {e.student.name:<25} {e.student.level:<14} "
            f"Grade: {self.format_grade(e.grade)}"
            for e in roster
        ]

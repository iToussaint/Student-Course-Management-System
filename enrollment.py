"""Enrollments linking students to courses, with grades and averages."""

from course import Course
from student import Student


class Enrollment:
    """A student's place in a course, with an optional grade.

    Args:
        student: The enrolled student.
        course: The course they are enrolled in.
    """

    def __init__(self, student: Student, course: Course) -> None:
        self._student = student
        self._course = course
        self._grade: float | None = None

    @property
    def student(self) -> Student:
        """The enrolled student (read-only)."""
        return self._student

    @property
    def course(self) -> Course:
        """The course (read-only)."""
        return self._course

    @property
    def grade(self) -> float | None:
        """The grade from 0 to 100, or None if not graded yet."""
        return self._grade

    @grade.setter
    def grade(self, value: float) -> None:
        if not Enrollment.is_valid_grade(value):
            raise ValueError("Grade must be between 0 and 100.")
        self._grade = value

    @staticmethod
    def is_valid_grade(value: float) -> bool:
        """Return True if value is an allowed grade (0 to 100)."""
        return 0 <= value <= 100

    def __repr__(self) -> str:
        return (
            f"Enrollment(student={self.student.id!r}, "
            f"course={self.course.code!r}, grade={self.grade!r})"
        )

    # Two enrollments are the same if they link the same student and course,
    # so the enrollments set keeps them unique.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Enrollment):
            return NotImplemented
        return (self.student, self.course) == (other.student, other.course)

    def __hash__(self) -> int:
        return hash((self.student, self.course))


# Set keeps enrollments unique
enrollments: set[Enrollment] = set()


def enroll_student(
    student: Student, *courses: Course
) -> tuple[list[Course], list[Course]]:
    """Enroll a student in one or more courses.

    Returns:
        (courses newly enrolled in, courses the student was already in).
    """
    enrolled, already = [], []
    for course in courses:
        enrollment = Enrollment(student, course)
        if enrollment in enrollments:  # fast set lookup via __hash__/__eq__
            already.append(course)
        else:
            enrollments.add(enrollment)
            enrolled.append(course)
    return enrolled, already


def find_enrollment(student: Student, course: Course) -> Enrollment | None:
    """Return the student's enrollment in the course, or None."""
    target = Enrollment(student, course)
    if target not in enrollments:
        return None
    # The set holds the original object (with its grade), so fetch that one
    return next(e for e in enrollments if e == target)


def remove_student(student: Student, course: Course) -> bool:
    """Remove a student from a course roster.

    Returns:
        True if removed, False if they weren't on the roster.
    """
    enrollment = find_enrollment(student, course)
    if enrollment is None:
        return False
    enrollments.remove(enrollment)
    return True


def get_roster(course: Course) -> list[Enrollment]:
    """Return the enrollments in a course, sorted by student name."""
    roster = [e for e in enrollments if e.course == course]
    return sorted(roster, key=lambda e: e.student.name)


def get_student_enrollments(student: Student) -> list[Enrollment]:
    """Return a student's enrollments, sorted by course code."""
    enrolled = [e for e in enrollments if e.student == student]
    return sorted(enrolled, key=lambda e: e.course.code)


def calculate_average(*scores: float) -> float | None:
    """Return the average of any number of scores, or None if none given."""
    if not scores:
        return None
    return sum(scores) / len(scores)


def course_average(course: Course) -> float | None:
    """Return the average grade in a course, ignoring ungraded students."""
    roster = get_roster(course)
    return calculate_average(*[e.grade for e in roster if e.grade is not None])


def student_average(student: Student) -> float | None:
    """Return a student's average grade, ignoring ungraded courses."""
    enrolled = get_student_enrollments(student)
    return calculate_average(
        *[e.grade for e in enrolled if e.grade is not None]
    )

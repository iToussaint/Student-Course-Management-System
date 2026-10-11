"""Enrollments and grades linking students to courses."""

from course import Course
from student import Student


class Enrollment:
    """A student's place in a course, with an optional grade."""

    def __init__(self, student: Student, course: Course) -> None:
        self._student = student
        self._course = course
        self._grade: float | None = None

    @property
    def student(self) -> Student:
        return self._student

    @property
    def course(self) -> Course:
        return self._course

    @property
    def grade(self) -> float | None:
        return self._grade

    @grade.setter
    def grade(self, value: float) -> None:
        if not Enrollment.is_valid_grade(value):
            raise ValueError("Grade must be between 0 and 100.")
        self._grade = value

    @staticmethod
    def is_valid_grade(value: float) -> bool:
        return 0 <= value <= 100

    def __repr__(self) -> str:
        return f"Enrollment(student={self.student.id!r}, course={self.course.code!r}, grade={self.grade!r})"

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


def enroll_student(student: Student, *courses: Course) -> tuple[list[Course], list[Course]]:
    """Enroll a student in one or more courses.

    Returns (newly enrolled courses, courses the student was already enrolled in).
    """
    enrolled, already = [], []
    for course in courses:
        enrollment = Enrollment(student, course)
        if enrollment in enrollments:
            already.append(course)
        else:
            enrollments.add(enrollment)
            enrolled.append(course)
    return enrolled, already


def find_enrollment(student: Student, course: Course) -> Enrollment | None:
    matches = [e for e in enrollments if e == Enrollment(student, course)]
    return matches[0] if matches else None


def remove_student(student: Student, course: Course) -> bool:
    """Remove a student from a course roster. Returns False if they weren't on it."""
    enrollment = find_enrollment(student, course)
    if enrollment is None:
        return False
    enrollments.remove(enrollment)
    return True


def get_roster(course: Course) -> list[Enrollment]:
    """Enrollments in a course, sorted by student name."""
    roster = [e for e in enrollments if e.course == course]
    return sorted(roster, key=lambda e: e.student.name)


def get_student_enrollments(student: Student) -> list[Enrollment]:
    """A student's enrollments, sorted by course code."""
    enrolled = [e for e in enrollments if e.student == student]
    return sorted(enrolled, key=lambda e: e.course.code)


def calculate_average(*scores: float) -> float | None:
    """Average of any number of scores, or None if there are none."""
    if not scores:
        return None
    return sum(scores) / len(scores)


def course_average(course: Course) -> float | None:
    return calculate_average(*[e.grade for e in get_roster(course) if e.grade is not None])


def student_average(student: Student) -> float | None:
    return calculate_average(*[e.grade for e in get_student_enrollments(student) if e.grade is not None])

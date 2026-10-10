"""Enrollments and grades linking students to courses."""

from course import courses
from student import get_student

# Sets keep each course's enrollments unique (course code -> student IDs)
enrollments: dict[str, set[str]] = {}
# Grades per course (course code -> student ID -> grade)
grades: dict[str, dict[str, float]] = {}


def enroll_student(student_id: str, *course_codes: str) -> tuple[list[str], list[str]]:
    """Enroll a student in one or more courses.

    Returns (newly enrolled codes, codes the student was already enrolled in).
    """
    enrolled, already = [], []
    for code in course_codes:
        roster = enrollments.setdefault(code.upper(), set())
        if student_id in roster:
            already.append(code.upper())
        else:
            roster.add(student_id)
            enrolled.append(code.upper())
    return enrolled, already


def remove_student(student_id: str, course_code: str) -> bool:
    """Remove a student from a course roster. Returns False if they weren't on it."""
    roster = enrollments.get(course_code.upper(), set())
    if student_id not in roster:
        return False
    roster.remove(student_id)
    grades.get(course_code.upper(), {}).pop(student_id, None)
    return True


def is_enrolled(student_id: str, course_code: str) -> bool:
    return student_id in enrollments.get(course_code.upper(), set())


def get_roster(course_code: str) -> list[dict[str, str]]:
    """Students enrolled in a course, sorted by name."""
    roster = [get_student(sid) for sid in enrollments.get(course_code.upper(), set())]
    return sorted((s for s in roster if s is not None), key=lambda s: s["name"])


def get_student_courses(student_id: str) -> list[dict[str, str]]:
    return [course for course in courses if is_enrolled(student_id, course["code"])]


def record_grade(student_id: str, course_code: str, grade: float) -> None:
    grades.setdefault(course_code.upper(), {})[student_id] = grade


def get_grade(student_id: str, course_code: str) -> float | None:
    return grades.get(course_code.upper(), {}).get(student_id)


def calculate_average(*scores: float) -> float | None:
    """Average of any number of scores, or None if there are none."""
    if not scores:
        return None
    return sum(scores) / len(scores)


def course_average(course_code: str) -> float | None:
    return calculate_average(*grades.get(course_code.upper(), {}).values())


def student_average(student_id: str) -> float | None:
    student_grades = [get_grade(student_id, course["code"]) for course in get_student_courses(student_id)]
    return calculate_average(*[grade for grade in student_grades if grade is not None])


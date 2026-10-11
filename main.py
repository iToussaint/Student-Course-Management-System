"""Student Course Management System - console application.

This module only handles input and output. The data and logic live in
student.py, course.py, enrollment.py, and report.py.
"""

from collections.abc import Callable

from course import Course, courses, get_course, load_sample_courses
from enrollment import (
    Enrollment,
    course_average,
    enroll_student,
    find_enrollment,
    remove_student,
)
from report import CourseRosterReport, Report, StudentSummaryReport
from student import (
    GraduateStudent,
    Student,
    UndergraduateStudent,
    add_student,
    get_student,
)

# A menu maps the key the user types to (label, action to run)
Menu = dict[str, tuple[str, Callable[[], None]]]

STUDENT_TYPES: dict[str, type[Student]] = {
    "1": UndergraduateStudent,
    "2": GraduateStudent,
}


# ---------- Input helpers ----------


def prompt_non_empty(message: str) -> str:
    """Keep asking until the user enters something, then return it."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def prompt_grade() -> float:
    """Keep asking until the user enters a grade between 0 and 100."""
    while True:
        value = prompt_non_empty("Enter grade (0-100): ")
        try:
            grade = float(value)
        except ValueError:
            print("Grade must be a number.")
            continue
        if Enrollment.is_valid_grade(grade):
            return grade
        print("Grade must be between 0 and 100.")


def prompt_student_type() -> type[Student]:
    """Keep asking until the user picks a valid student type."""
    while True:
        choice = prompt_non_empty(
            "Student type - 1. Undergraduate  2. Graduate: "
        )
        if choice in STUDENT_TYPES:
            return STUDENT_TYPES[choice]
        print("Invalid option. Please enter 1 or 2.")


def find_student() -> Student | None:
    """Ask for a student ID and return that student, or None if unknown."""
    student_id = prompt_non_empty("Enter student ID: ")
    student = get_student(student_id)
    if student is None:
        print(f"No student found with ID {student_id.upper()}.")
    return student


def find_course() -> Course | None:
    """Show the courses, ask for a code, and return it, or None if unknown."""
    show_courses()
    code = prompt_non_empty("Enter course code: ")
    course = get_course(code)
    if course is None:
        print(f"No course found with code {code.upper()}.")
    return course


def find_course_and_student() -> tuple[Course, Student] | None:
    """Ask for a course, then a student; return None if either is unknown."""
    course = find_course()
    if course is None:
        return None
    student = find_student()
    if student is None:
        return None
    return course, student


# ---------- Output helpers ----------


def show_courses() -> None:
    """Print every available course."""
    print("\nAvailable courses:")
    for course in courses:
        print(f"  {course.code:<8} {course.title}")


def show_report(report: Report) -> None:
    """Print any kind of report; each Report subclass builds its own."""
    print()
    print(report.generate())


# ---------- Student actions ----------


def register_student() -> None:
    """Register a new student of the chosen type."""
    name = prompt_non_empty("Enter your full name: ")
    student = add_student(name, prompt_student_type())
    print(f"Registered {student.name} ({student.level}) with ID {student.id}.")


def enroll_in_courses() -> None:
    """Enroll a student in one or more courses entered on one line."""
    student = find_student()
    if student is None:
        return
    show_courses()
    entered = prompt_non_empty("Enter course code(s), separated by spaces: ")
    # dict.fromkeys drops repeated codes but keeps the order they were typed
    codes = list(dict.fromkeys(entered.upper().split()))

    valid: list[Course] = []
    unknown: list[str] = []
    for code in codes:
        course = get_course(code)
        if course is None:
            unknown.append(code)
        else:
            valid.append(course)

    enrolled, already = enroll_student(student, *valid)
    if enrolled:
        print(f"Enrolled in: {', '.join(c.code for c in enrolled)}")
    if already:
        print(f"Already enrolled in: {', '.join(c.code for c in already)}")
    if unknown:
        print(f"Unknown course code(s): {', '.join(unknown)}")


def view_student_summary() -> None:
    """Show a student's courses, grades, and average."""
    student = find_student()
    if student is not None:
        show_report(StudentSummaryReport(student))


# ---------- Instructor actions ----------


def view_roster() -> None:
    """Show everyone enrolled in a course."""
    course = find_course()
    if course is not None:
        show_report(CourseRosterReport(course))


def add_to_roster() -> None:
    """Add a student to a course roster."""
    selection = find_course_and_student()
    if selection is None:
        return
    course, student = selection
    enrolled, _ = enroll_student(student, course)
    if enrolled:
        print(f"Added {student.name} to {course.code}.")
    else:
        print(f"{student.name} is already on the {course.code} roster.")


def remove_from_roster() -> None:
    """Remove a student (and their grade) from a course roster."""
    selection = find_course_and_student()
    if selection is None:
        return
    course, student = selection
    if remove_student(student, course):
        print(f"Removed {student.name} from {course.code}.")
    else:
        print(f"{student.name} is not on the {course.code} roster.")


def enter_grade() -> None:
    """Record a grade for a student enrolled in a course."""
    selection = find_course_and_student()
    if selection is None:
        return
    course, student = selection
    enrollment = find_enrollment(student, course)
    if enrollment is None:
        print(f"{student.name} is not enrolled in {course.code}.")
        return
    enrollment.grade = prompt_grade()
    print(
        f"Recorded {enrollment.grade:.1f} for {student.name} in {course.code}."
    )


def view_course_average() -> None:
    """Show the average grade for a course."""
    course = find_course()
    if course is None:
        return
    average = course_average(course)
    if average is None:
        print(f"No grades recorded for {course.code} yet.")
    else:
        print(f"Average grade for {course.code}: {average:.1f}")


# ---------- Menus ----------


def run_menu(title: str, options: Menu, exit_label: str = "Back") -> None:
    """Show a menu and run the chosen action until the user picks 0."""
    while True:
        print(f"\n--- {title} ---")
        for key, (label, _) in options.items():
            print(f"{key}. {label}")
        print(f"0. {exit_label}")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            return
        if choice in options:
            _, action = options[choice]
            action()
        else:
            print("Invalid option. Please try again.")


STUDENT_MENU: Menu = {
    "1": ("Register", register_student),
    "2": ("Enroll in courses", enroll_in_courses),
    "3": ("View summary", view_student_summary),
}

INSTRUCTOR_MENU: Menu = {
    "1": ("View course roster", view_roster),
    "2": ("Add student to roster", add_to_roster),
    "3": ("Remove student from roster", remove_from_roster),
    "4": ("Record grade", enter_grade),
    "5": ("View course average", view_course_average),
}

MAIN_MENU: Menu = {
    "1": ("Student", lambda: run_menu("Student Menu", STUDENT_MENU)),
    "2": ("Instructor", lambda: run_menu("Instructor Menu", INSTRUCTOR_MENU)),
}


def main() -> None:
    """Start the application and run the main menu."""
    load_sample_courses()
    print("Welcome to the Student Course Management System")
    try:
        run_menu("Main Menu", MAIN_MENU, exit_label="Exit")
    except (KeyboardInterrupt, EOFError):
        print()  # Ctrl+C or end of input: finish the line, then exit cleanly
    print("Goodbye!")


if __name__ == "__main__":
    main()

"""Student Course Management System - console application.

This module only handles input and output. The data and logic live in
student.py, course.py, enrollment.py, and report.py.
"""

from collections.abc import Callable

from course import Course, CourseCatalog, load_sample_courses
from enrollment import Enrollment, EnrollmentRegistry
from report import CourseRosterReport, Report, StudentSummaryReport
from student import (
    GraduateStudent,
    Student,
    StudentRegistry,
    UndergraduateStudent,
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


def show_report(report: Report) -> None:
    """Print any kind of report; each Report subclass builds its own."""
    print()
    print(report.generate())


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


class ConsoleApp:
    """The console menus and the actions behind them.

    The registries are passed in rather than created here, so the app
    only talks to the user and leaves storage to them.

    Args:
        students: Where students are registered and looked up.
        catalog: The courses on offer.
        enrollments: Where enrollments and grades are kept.
    """

    def __init__(
        self,
        students: StudentRegistry,
        catalog: CourseCatalog,
        enrollments: EnrollmentRegistry,
    ) -> None:
        self._students = students
        self._catalog = catalog
        self._enrollments = enrollments

    def run(self) -> None:
        """Run the main menu until the user exits."""
        student_menu: Menu = {
            "1": ("Register", self.register_student),
            "2": ("Enroll in courses", self.enroll_in_courses),
            "3": ("View summary", self.view_student_summary),
        }
        instructor_menu: Menu = {
            "1": ("View course roster", self.view_roster),
            "2": ("Add student to roster", self.add_to_roster),
            "3": ("Remove student from roster", self.remove_from_roster),
            "4": ("Record grade", self.enter_grade),
            "5": ("View course average", self.view_course_average),
        }
        main_menu: Menu = {
            "1": ("Student", lambda: run_menu("Student Menu", student_menu)),
            "2": (
                "Instructor",
                lambda: run_menu("Instructor Menu", instructor_menu),
            ),
        }
        run_menu("Main Menu", main_menu, exit_label="Exit")

    # ---------- Lookup helpers ----------

    def _find_student(self) -> Student | None:
        """Ask for a student ID and return that student, or None."""
        student_id = prompt_non_empty("Enter student ID: ")
        student = self._students.get(student_id)
        if student is None:
            print(f"No student found with ID {student_id.upper()}.")
        return student

    def _find_course(self) -> Course | None:
        """Show the courses, ask for a code, and return it, or None."""
        self._show_courses()
        code = prompt_non_empty("Enter course code: ")
        course = self._catalog.get(code)
        if course is None:
            print(f"No course found with code {code.upper()}.")
        return course

    def _find_course_and_student(self) -> tuple[Course, Student] | None:
        """Ask for a course, then a student; None if either is unknown."""
        course = self._find_course()
        if course is None:
            return None
        student = self._find_student()
        if student is None:
            return None
        return course, student

    def _show_courses(self) -> None:
        """Print every available course."""
        print("\nAvailable courses:")
        for course in self._catalog:
            print(f"  {course.code:<8} {course.title}")

    # ---------- Student actions ----------

    def register_student(self) -> None:
        """Register a new student of the chosen type."""
        name = prompt_non_empty("Enter your full name: ")
        student = self._students.add_student(name, prompt_student_type())
        print(
            f"Registered {student.name} ({student.level}) "
            f"with ID {student.id}."
        )

    def enroll_in_courses(self) -> None:
        """Enroll a student in one or more courses entered on one line."""
        student = self._find_student()
        if student is None:
            return
        self._show_courses()
        entered = prompt_non_empty(
            "Enter course code(s), separated by spaces: "
        )
        # Map each typed code to its course (None if unknown). Dict keys are
        # unique, so repeated codes are dropped but the typed order is kept.
        found = {
            code: self._catalog.get(code) for code in entered.upper().split()
        }
        valid = [course for course in found.values() if course is not None]
        unknown = [code for code, course in found.items() if course is None]

        enrolled, already = self._enrollments.enroll_student(student, *valid)
        if enrolled:
            print(f"Enrolled in: {', '.join(c.code for c in enrolled)}")
        if already:
            print(f"Already enrolled in: {', '.join(c.code for c in already)}")
        if unknown:
            print(f"Unknown course code(s): {', '.join(unknown)}")

    def view_student_summary(self) -> None:
        """Show a student's courses, grades, and average."""
        student = self._find_student()
        if student is not None:
            show_report(StudentSummaryReport(student, self._enrollments))

    # ---------- Instructor actions ----------

    def view_roster(self) -> None:
        """Show everyone enrolled in a course."""
        course = self._find_course()
        if course is not None:
            show_report(CourseRosterReport(course, self._enrollments))

    def add_to_roster(self) -> None:
        """Add a student to a course roster."""
        selection = self._find_course_and_student()
        if selection is None:
            return
        course, student = selection
        enrolled, _ = self._enrollments.enroll_student(student, course)
        if enrolled:
            print(f"Added {student.name} to {course.code}.")
        else:
            print(f"{student.name} is already on the {course.code} roster.")

    def remove_from_roster(self) -> None:
        """Remove a student (and their grade) from a course roster."""
        selection = self._find_course_and_student()
        if selection is None:
            return
        course, student = selection
        if self._enrollments.remove(student, course):
            print(f"Removed {student.name} from {course.code}.")
        else:
            print(f"{student.name} is not on the {course.code} roster.")

    def enter_grade(self) -> None:
        """Record a grade for a student enrolled in a course."""
        selection = self._find_course_and_student()
        if selection is None:
            return
        course, student = selection
        enrollment = self._enrollments.find(student, course)
        if enrollment is None:
            print(f"{student.name} is not enrolled in {course.code}.")
            return
        enrollment.grade = prompt_grade()
        print(
            f"Recorded {enrollment.grade:.1f} for {student.name} "
            f"in {course.code}."
        )

    def view_course_average(self) -> None:
        """Show the average grade for a course."""
        course = self._find_course()
        if course is None:
            return
        average = self._enrollments.course_average(course)
        if average is None:
            print(f"No grades recorded for {course.code} yet.")
        else:
            print(f"Average grade for {course.code}: {average:.1f}")


def main() -> None:
    """Build the registries, then start the application."""
    catalog = CourseCatalog()
    load_sample_courses(catalog)
    app = ConsoleApp(StudentRegistry(), catalog, EnrollmentRegistry())
    print("Welcome to the Student Course Management System")
    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        print()  # Ctrl+C or end of input: finish the line, then exit cleanly
    print("Goodbye!")


if __name__ == "__main__":
    main()

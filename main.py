"""Student Course Management System - console application."""

from course import Course, courses, get_course
from enrollment import course_average, enroll_student, find_enrollment, remove_student
from report import CourseRosterReport, Report, StudentSummaryReport
from student import (
    GraduateStudent,
    Student,
    UndergraduateStudent,
    add_student,
    get_student,
)


def prompt_non_empty(message: str) -> str:
    """Keep asking until the user enters something."""
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
        if 0 <= grade <= 100:
            return grade
        print("Grade must be between 0 and 100.")


def prompt_student_type() -> type[Student]:
    """Keep asking until the user picks undergraduate or graduate."""
    while True:
        choice = prompt_non_empty("Student type - 1. Undergraduate  2. Graduate: ")
        if choice == "1":
            return UndergraduateStudent
        if choice == "2":
            return GraduateStudent
        print("Invalid option. Please enter 1 or 2.")


def find_student() -> Student | None:
    student_id = prompt_non_empty("Enter student ID: ")
    student = get_student(student_id)
    if student is None:
        print(f"No student found with ID {student_id.upper()}.")
    return student


def find_course() -> Course | None:
    show_courses()
    code = prompt_non_empty("Enter course code: ")
    course = get_course(code)
    if course is None:
        print(f"No course found with code {code.upper()}.")
    return course


def show_courses() -> None:
    print("\nAvailable courses:")
    for course in courses:
        print(f"  {course.code:<8} {course.title}")


def show_report(report: Report) -> None:
    print()
    print(report.generate())


# ---------- Student actions ----------

def register_student() -> None:
    name = prompt_non_empty("Enter your full name: ")
    student_type = prompt_student_type()
    student = add_student(name, student_type)
    print(f"Registered {student.name} ({student.level}) with ID {student.id}.")


def enroll_in_courses() -> None:
    student = find_student()
    if student is None:
        return
    show_courses()
    codes = prompt_non_empty("Enter course code(s), separated by spaces: ").upper().split()
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
    student = find_student()
    if student is None:
        return
    show_report(StudentSummaryReport(student))


# ---------- Instructor actions ----------

def view_roster() -> None:
    course = find_course()
    if course is None:
        return
    show_report(CourseRosterReport(course))


def add_to_roster() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    enrolled, _ = enroll_student(student, course)
    if enrolled:
        print(f"Added {student.name} to {course.code}.")
    else:
        print(f"{student.name} is already on the {course.code} roster.")


def remove_from_roster() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    if remove_student(student, course):
        print(f"Removed {student.name} from {course.code}.")
    else:
        print(f"{student.name} is not on the {course.code} roster.")


def enter_grade() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    enrollment = find_enrollment(student, course)
    if enrollment is None:
        print(f"{student.name} is not enrolled in {course.code}.")
        return
    enrollment.grade = prompt_grade()
    print(f"Recorded {enrollment.grade:.1f} for {student.name} in {course.code}.")


def view_course_average() -> None:
    course = find_course()
    if course is None:
        return
    average = course_average(course)
    if average is None:
        print(f"No grades recorded for {course.code} yet.")
    else:
        print(f"Average grade for {course.code}: {average:.1f}")


# ---------- Menus ----------

def student_menu() -> None:
    while True:
        print("\n--- Student Menu ---")
        print("1. Register")
        print("2. Enroll in courses")
        print("3. View summary")
        print("0. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_student()
        elif choice == "2":
            enroll_in_courses()
        elif choice == "3":
            view_student_summary()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def instructor_menu() -> None:
    while True:
        print("\n--- Instructor Menu ---")
        print("1. View course roster")
        print("2. Add student to roster")
        print("3. Remove student from roster")
        print("4. Record grade")
        print("5. View course average")
        print("0. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            view_roster()
        elif choice == "2":
            add_to_roster()
        elif choice == "3":
            remove_from_roster()
        elif choice == "4":
            enter_grade()
        elif choice == "5":
            view_course_average()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def main() -> None:
    print("Welcome to the Student Course Management System")
    while True:
        print("\n=== Main Menu ===")
        print("1. Student")
        print("2. Instructor")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            student_menu()
        elif choice == "2":
            instructor_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

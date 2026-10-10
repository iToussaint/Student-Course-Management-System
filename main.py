"""Student Course Management System - console application."""

from course import courses, get_course
from enrollment import (
    course_average,
    enroll_student,
    get_grade,
    get_roster,
    get_student_courses,
    is_enrolled,
    record_grade,
    remove_student,
    student_average,
)
from student import add_student, get_student


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


def find_student() -> dict[str, str] | None:
    student_id = prompt_non_empty("Enter student ID: ")
    student = get_student(student_id)
    if student is None:
        print(f"No student found with ID {student_id.upper()}.")
    return student


def find_course() -> dict[str, str] | None:
    show_courses()
    code = prompt_non_empty("Enter course code: ")
    course = get_course(code)
    if course is None:
        print(f"No course found with code {code.upper()}.")
    return course


def show_courses() -> None:
    print("\nAvailable courses:")
    for course in courses:
        print(f"  {course['code']:<8} {course['title']}")


def format_grade(grade: float | None) -> str:
    return "-" if grade is None else f"{grade:.1f}"


# ---------- Student actions ----------

def register_student() -> None:
    name = prompt_non_empty("Enter your full name: ")
    student = add_student(name)
    print(f"Registered {student['name']} with ID {student['id']}.")


def enroll_in_courses() -> None:
    student = find_student()
    if student is None:
        return
    show_courses()
    codes = prompt_non_empty("Enter course code(s), separated by spaces: ").upper().split()
    unknown = [code for code in codes if get_course(code) is None]
    valid = [code for code in codes if get_course(code) is not None]
    enrolled, already = enroll_student(student["id"], *valid)
    if enrolled:
        print(f"Enrolled in: {', '.join(enrolled)}")
    if already:
        print(f"Already enrolled in: {', '.join(already)}")
    if unknown:
        print(f"Unknown course code(s): {', '.join(unknown)}")


def view_student_summary() -> None:
    student = find_student()
    if student is None:
        return
    enrolled = get_student_courses(student["id"])
    student_grades = {course["code"]: get_grade(student["id"], course["code"]) for course in enrolled}
    print(f"\nSummary for {student['name']} ({student['id']})")
    print(f"Courses enrolled: {len(enrolled)}")
    for course in enrolled:
        print(f"  {course['code']:<8} {course['title']:<30} Grade: {format_grade(student_grades[course['code']])}")
    print(f"Average grade: {format_grade(student_average(student['id']))}")


# ---------- Instructor actions ----------

def view_roster() -> None:
    course = find_course()
    if course is None:
        return
    roster = get_roster(course["code"])
    print(f"\nRoster for {course['code']} - {course['title']} ({len(roster)} students)")
    if not roster:
        print("  No students enrolled.")
    for student in roster:
        grade = get_grade(student["id"], course["code"])
        print(f"  {student['id']}  {student['name']:<25} Grade: {format_grade(grade)}")


def add_to_roster() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    enrolled, _ = enroll_student(student["id"], course["code"])
    if enrolled:
        print(f"Added {student['name']} to {course['code']}.")
    else:
        print(f"{student['name']} is already on the {course['code']} roster.")


def remove_from_roster() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    if remove_student(student["id"], course["code"]):
        print(f"Removed {student['name']} from {course['code']}.")
    else:
        print(f"{student['name']} is not on the {course['code']} roster.")


def enter_grade() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    if not is_enrolled(student["id"], course["code"]):
        print(f"{student['name']} is not enrolled in {course['code']}.")
        return
    grade = prompt_grade()
    record_grade(student["id"], course["code"], grade)
    print(f"Recorded {grade:.1f} for {student['name']} in {course['code']}.")


def view_course_average() -> None:
    course = find_course()
    if course is None:
        return
    average = course_average(course["code"])
    if average is None:
        print(f"No grades recorded for {course['code']} yet.")
    else:
        print(f"Average grade for {course['code']}: {average:.1f}")


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

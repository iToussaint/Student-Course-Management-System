"""Student Course Management System - console application."""

# Lists store the collections
students: list[dict[str, str]] = []
courses: list[dict[str, str]] = [
    {"code": "CS101", "title": "Introduction to Programming"},
    {"code": "MATH201", "title": "Linear Algebra"},
    {"code": "PHY110", "title": "General Physics"},
]

# Dictionaries map IDs to objects
students_by_id: dict[str, dict[str, str]] = {}
courses_by_code: dict[str, dict[str, str]] = {course["code"]: course for course in courses}

# Sets keep each course's enrollments unique (course code -> student IDs)
enrollments: dict[str, set[str]] = {course["code"]: set() for course in courses}


def prompt_non_empty(message: str) -> str:
    """Keep asking until the user enters something."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def find_student() -> dict[str, str] | None:
    student_id = prompt_non_empty("Enter student ID: ").upper()
    student = students_by_id.get(student_id)
    if student is None:
        print(f"No student found with ID {student_id}.")
    return student


def find_course() -> dict[str, str] | None:
    show_courses()
    code = prompt_non_empty("Enter course code: ").upper()
    course = courses_by_code.get(code)
    if course is None:
        print(f"No course found with code {code}.")
    return course


def show_courses() -> None:
    print("\nAvailable courses:")
    for course in courses:
        print(f"  {course['code']:<8} {course['title']}")


# ---------- Student actions ----------

def register_student() -> None:
    name = prompt_non_empty("Enter your full name: ")
    student_id = f"S{len(students) + 1:03d}"
    student = {"id": student_id, "name": name}
    students.append(student)
    students_by_id[student_id] = student
    print(f"Registered {name} with ID {student_id}.")


def enroll_in_course() -> None:
    student = find_student()
    if student is None:
        return
    course = find_course()
    if course is None:
        return
    roster = enrollments[course["code"]]
    if student["id"] in roster:
        print(f"{student['name']} is already enrolled in {course['code']}.")
    else:
        roster.add(student["id"])
        print(f"{student['name']} enrolled in {course['code']}.")


def view_student_summary() -> None:
    student = find_student()
    if student is None:
        return
    enrolled = {
        course["code"]: course["title"]
        for course in courses
        if student["id"] in enrollments[course["code"]]
    }
    print(f"\nSummary for {student['name']} ({student['id']})")
    print(f"Courses enrolled: {len(enrolled)}")
    for code, title in enrolled.items():
        print(f"  {code:<8} {title}")


# ---------- Instructor actions ----------

def view_roster() -> None:
    course = find_course()
    if course is None:
        return
    names = sorted(students_by_id[sid]["name"] for sid in enrollments[course["code"]])
    print(f"\nRoster for {course['code']} - {course['title']} ({len(names)} students)")
    if not names:
        print("  No students enrolled.")
    for name in names:
        print(f"  {name}")


def add_to_roster() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    roster = enrollments[course["code"]]
    if student["id"] in roster:
        print(f"{student['name']} is already on the {course['code']} roster.")
    else:
        roster.add(student["id"])
        print(f"Added {student['name']} to {course['code']}.")


def remove_from_roster() -> None:
    course = find_course()
    if course is None:
        return
    student = find_student()
    if student is None:
        return
    roster = enrollments[course["code"]]
    if student["id"] in roster:
        roster.remove(student["id"])
        print(f"Removed {student['name']} from {course['code']}.")
    else:
        print(f"{student['name']} is not on the {course['code']} roster.")


# ---------- Menus ----------

def student_menu() -> None:
    while True:
        print("\n--- Student Menu ---")
        print("1. Register")
        print("2. Enroll in a course")
        print("3. View summary")
        print("0. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_student()
        elif choice == "2":
            enroll_in_course()
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
        print("0. Back")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            view_roster()
        elif choice == "2":
            add_to_roster()
        elif choice == "3":
            remove_from_roster()
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

"""Student records."""

# List stores the collection, dictionary maps IDs to students
students: list[dict[str, str]] = []
students_by_id: dict[str, dict[str, str]] = {}


def add_student(name: str, **details: str) -> dict[str, str]:
    """Register a new student and return it.

    Any extra keyword arguments (e.g. email="...") are stored on the student.
    """
    student_id = f"S{len(students) + 1:03d}"
    student = {"id": student_id, "name": name, **details}
    students.append(student)
    students_by_id[student_id] = student
    return student


def get_student(student_id: str) -> dict[str, str] | None:
    return students_by_id.get(student_id.upper())

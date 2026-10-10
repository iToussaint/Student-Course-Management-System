"""Course catalogue."""

# List stores the collection, dictionary maps codes to courses
courses: list[dict[str, str]] = []
courses_by_code: dict[str, dict[str, str]] = {}


def add_course(code: str, title: str) -> dict[str, str]:
    course = {"code": code.upper(), "title": title}
    courses.append(course)
    courses_by_code[course["code"]] = course
    return course


def get_course(code: str) -> dict[str, str] | None:
    return courses_by_code.get(code.upper())


add_course("CS101", "Introduction to Programming")
add_course("MATH201", "Linear Algebra")
add_course("PHY110", "General Physics")

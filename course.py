"""Course catalogue."""


class Course:
    def __init__(self, code: str, title: str) -> None:
        self._code = code.upper()
        self._title = title

    @property
    def code(self) -> str:
        return self._code

    @property
    def title(self) -> str:
        return self._title

    def __repr__(self) -> str:
        return f"Course(code={self.code!r}, title={self.title!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Course):
            return NotImplemented
        return self.code == other.code

    def __hash__(self) -> int:
        return hash(self.code)


# List stores the collection, dictionary maps codes to courses
courses: list[Course] = []
courses_by_code: dict[str, Course] = {}


def add_course(code: str, title: str) -> Course:
    course = Course(code, title)
    courses.append(course)
    courses_by_code[course.code] = course
    return course


def get_course(code: str) -> Course | None:
    return courses_by_code.get(code.upper())


add_course("CS101", "Introduction to Programming")
add_course("MATH201", "Linear Algebra")
add_course("PHY110", "General Physics")

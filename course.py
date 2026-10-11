"""Course catalogue: the Course class and the course registry."""


class Course:
    """A course students can enroll in.

    Args:
        code: Unique course code such as "CS101" (stored in upper case).
        title: Human-readable course title.
    """

    def __init__(self, code: str, title: str) -> None:
        self._code = code.upper()
        self._title = title

    @property
    def code(self) -> str:
        """The course code (read-only)."""
        return self._code

    @property
    def title(self) -> str:
        """The course title (read-only)."""
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
    """Create a course, store it, and return it."""
    course = Course(code, title)
    courses.append(course)
    courses_by_code[course.code] = course
    return course


def get_course(code: str) -> Course | None:
    """Return the course with this code (case-insensitive), or None."""
    return courses_by_code.get(code.upper())


def load_sample_courses() -> None:
    """Add the courses offered when the application starts."""
    add_course("CS101", "Introduction to Programming")
    add_course("MATH201", "Linear Algebra")
    add_course("PHY110", "General Physics")

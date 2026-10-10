"""Course catalogue: the Course class and the course catalogue."""

from collections.abc import Iterator


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


class CourseCatalog:
    """Stores the available courses and looks them up by code."""

    def __init__(self) -> None:
        # List stores the collection, dictionary maps codes to courses
        self._courses: list[Course] = []
        self._courses_by_code: dict[str, Course] = {}

    def add_course(self, code: str, title: str) -> Course:
        """Create a course, store it, and return it."""
        course = Course(code, title)
        self._courses.append(course)
        self._courses_by_code[course.code] = course
        return course

    def get(self, code: str) -> Course | None:
        """Return the course with this code (case-insensitive), or None."""
        return self._courses_by_code.get(code.upper())

    def __iter__(self) -> Iterator[Course]:
        return iter(self._courses)


def load_sample_courses(catalog: CourseCatalog) -> None:
    """Add the courses offered when the application starts."""
    catalog.add_course("CS101", "Introduction to Programming")
    catalog.add_course("MATH201", "Linear Algebra")
    catalog.add_course("PHY110", "General Physics")

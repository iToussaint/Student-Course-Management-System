"""Tests for the Course class and the course catalogue."""

import unittest

from course import Course, CourseCatalog, load_sample_courses


class CourseTest(unittest.TestCase):
    """Behaviour of a single Course."""

    def test_code_is_stored_in_upper_case(self) -> None:
        """Course codes are normalised to upper case."""
        self.assertEqual(Course("cs101", "Programming").code, "CS101")

    def test_courses_are_equal_by_code(self) -> None:
        """Two courses with the same code compare equal."""
        self.assertEqual(Course("CS101", "A"), Course("cs101", "B"))

    def test_repr_shows_code_and_title(self) -> None:
        """__repr__ shows the code and title."""
        self.assertEqual(
            repr(Course("CS101", "Programming")),
            "Course(code='CS101', title='Programming')",
        )


class CourseCatalogTest(unittest.TestCase):
    """Adding, listing, and looking up courses."""

    def setUp(self) -> None:
        """Start each test with the sample courses."""
        self.catalog = CourseCatalog()
        load_sample_courses(self.catalog)

    def test_sample_courses_are_listed_in_order(self) -> None:
        """Iterating the catalogue gives courses in the order added."""
        self.assertEqual(
            [course.code for course in self.catalog],
            ["CS101", "MATH201", "PHY110"],
        )

    def test_get_is_case_insensitive(self) -> None:
        """Codes can be looked up in any case."""
        course = self.catalog.get("math201")
        self.assertIsNotNone(course)
        assert course is not None  # narrows the type for mypy
        self.assertEqual(course.title, "Linear Algebra")

    def test_get_unknown_code_returns_none(self) -> None:
        """An unknown code returns None."""
        self.assertIsNone(self.catalog.get("XX100"))


if __name__ == "__main__":
    unittest.main()

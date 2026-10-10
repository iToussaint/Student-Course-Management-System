"""Tests for enrollments, grades, and averages."""

import unittest

from course import Course
from enrollment import Enrollment, EnrollmentRegistry, calculate_average
from student import GraduateStudent, Student, UndergraduateStudent


class EnrollmentTest(unittest.TestCase):
    """Grade validation and equality of a single Enrollment."""

    def setUp(self) -> None:
        """Create an ungraded enrollment."""
        self.student = UndergraduateStudent("S001", "Ana")
        self.course = Course("CS101", "Programming")
        self.enrollment = Enrollment(self.student, self.course)

    def test_new_enrollment_has_no_grade(self) -> None:
        """A new enrollment starts ungraded."""
        self.assertIsNone(self.enrollment.grade)

    def test_grade_accepts_the_full_range(self) -> None:
        """0 and 100 are both allowed."""
        for grade in (0, 100, 72.5):
            self.enrollment.grade = grade
            self.assertEqual(self.enrollment.grade, grade)

    def test_grade_outside_range_is_rejected(self) -> None:
        """Grades below 0 or above 100 raise ValueError."""
        for grade in (-1, 100.5):
            with self.assertRaises(ValueError):
                self.enrollment.grade = grade

    def test_same_student_and_course_are_equal(self) -> None:
        """Enrollments compare by student and course, not grade."""
        other = Enrollment(self.student, self.course)
        other.grade = 90
        self.assertEqual(self.enrollment, other)
        self.assertEqual(hash(self.enrollment), hash(other))


class CalculateAverageTest(unittest.TestCase):
    """The calculate_average helper."""

    def test_average_of_several_scores(self) -> None:
        """Any number of scores can be passed."""
        self.assertEqual(calculate_average(70, 80, 90), 80)

    def test_no_scores_returns_none(self) -> None:
        """With no scores there is no average."""
        self.assertIsNone(calculate_average())


class EnrollmentRegistryTest(unittest.TestCase):
    """Enrolling, removing, rosters, and averages."""

    def setUp(self) -> None:
        """Create two students, two courses, and an empty registry."""
        self.ana = UndergraduateStudent("S001", "Ana")
        self.ben = GraduateStudent("S002", "Ben")
        self.cs = Course("CS101", "Programming")
        self.math = Course("MATH201", "Linear Algebra")
        self.enrollments = EnrollmentRegistry()

    def test_enroll_in_several_courses(self) -> None:
        """All new courses are reported as enrolled."""
        enrolled, already = self.enrollments.enroll_student(
            self.ana, self.cs, self.math
        )
        self.assertEqual(enrolled, [self.cs, self.math])
        self.assertEqual(already, [])

    def test_enrolling_twice_is_reported_not_duplicated(self) -> None:
        """A repeat enrollment is reported and not stored again."""
        self.enrollments.enroll_student(self.ana, self.cs)
        enrolled, already = self.enrollments.enroll_student(
            self.ana, self.cs, self.math
        )
        self.assertEqual(enrolled, [self.math])
        self.assertEqual(already, [self.cs])
        self.assertEqual(len(self.enrollments.roster(self.cs)), 1)

    def test_find_returns_the_stored_enrollment(self) -> None:
        """The stored enrollment is returned, so its grade is kept."""
        self.enrollments.enroll_student(self.ana, self.cs)
        found = self.enrollments.find(self.ana, self.cs)
        assert found is not None
        found.grade = 88
        again = self.enrollments.find(self.ana, self.cs)
        assert again is not None
        self.assertEqual(again.grade, 88)

    def test_find_when_not_enrolled_returns_none(self) -> None:
        """Looking up a student not in the course returns None."""
        self.assertIsNone(self.enrollments.find(self.ana, self.cs))

    def test_remove(self) -> None:
        """Removing works once, then reports the student is not there."""
        self.enrollments.enroll_student(self.ana, self.cs)
        self.assertTrue(self.enrollments.remove(self.ana, self.cs))
        self.assertFalse(self.enrollments.remove(self.ana, self.cs))
        self.assertEqual(self.enrollments.roster(self.cs), [])

    def test_roster_is_sorted_by_name(self) -> None:
        """The roster lists students alphabetically."""
        self.enrollments.enroll_student(self.ben, self.cs)
        self.enrollments.enroll_student(self.ana, self.cs)
        self.assertEqual(
            [e.student for e in self.enrollments.roster(self.cs)],
            [self.ana, self.ben],
        )

    def test_student_enrollments_are_sorted_by_code(self) -> None:
        """A student's enrollments are listed by course code."""
        self.enrollments.enroll_student(self.ana, self.math, self.cs)
        self.assertEqual(
            [e.course for e in self.enrollments.for_student(self.ana)],
            [self.cs, self.math],
        )

    def _grade(self, student: Student, course: Course, grade: float) -> None:
        """Enroll a student and record a grade."""
        self.enrollments.enroll_student(student, course)
        enrollment = self.enrollments.find(student, course)
        assert enrollment is not None
        enrollment.grade = grade

    def test_course_average_ignores_ungraded_students(self) -> None:
        """Only graded students count towards the course average."""
        self._grade(self.ana, self.cs, 80)
        self._grade(self.ben, self.cs, 90)
        self.enrollments.enroll_student(
            UndergraduateStudent("S003", "Cleo"), self.cs
        )
        self.assertEqual(self.enrollments.course_average(self.cs), 85)

    def test_student_average_ignores_ungraded_courses(self) -> None:
        """Only graded courses count towards a student's average."""
        self._grade(self.ana, self.cs, 70)
        self.enrollments.enroll_student(self.ana, self.math)
        self.assertEqual(self.enrollments.student_average(self.ana), 70)

    def test_averages_without_grades_are_none(self) -> None:
        """No grades means no average."""
        self.enrollments.enroll_student(self.ana, self.cs)
        self.assertIsNone(self.enrollments.course_average(self.cs))
        self.assertIsNone(self.enrollments.student_average(self.ana))


if __name__ == "__main__":
    unittest.main()

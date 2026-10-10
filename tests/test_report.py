"""Tests for the report classes."""

import unittest

from course import Course
from enrollment import EnrollmentRegistry
from report import CourseRosterReport, Report, StudentSummaryReport
from student import GraduateStudent, UndergraduateStudent


class ReportTest(unittest.TestCase):
    """The text each report generates."""

    def setUp(self) -> None:
        """Enroll a graduate and an undergraduate; grade one of them."""
        self.ana = GraduateStudent("S001", "Alice Uwase")
        self.ben = UndergraduateStudent("S002", "Ben Habimana")
        self.cs = Course("CS101", "Introduction to Programming")
        self.math = Course("MATH201", "Linear Algebra")
        self.enrollments = EnrollmentRegistry()
        self.enrollments.enroll_student(self.ana, self.cs, self.math)
        self.enrollments.enroll_student(self.ben, self.cs)
        enrollment = self.enrollments.find(self.ana, self.cs)
        assert enrollment is not None
        enrollment.grade = 85

    def test_report_is_abstract(self) -> None:
        """The Report base class cannot be created directly."""
        with self.assertRaises(TypeError):
            Report()  # type: ignore[abstract]

    def test_format_grade(self) -> None:
        """Grades show one decimal place, or "-" when missing."""
        self.assertEqual(Report.format_grade(85), "85.0")
        self.assertEqual(Report.format_grade(None), "-")

    def test_student_summary(self) -> None:
        """The summary lists courses, grades, and the average."""
        report = StudentSummaryReport(self.ana, self.enrollments)
        self.assertEqual(
            report.generate().splitlines(),
            [
                "Summary for Alice Uwase (S001, Graduate)",
                "----------------------------------------",
                "Courses enrolled: 2",
                "  CS101    Introduction to Programming    Grade: 85.0",
                "  MATH201  Linear Algebra                 Grade: -",
                "Average grade: 85.0",
            ],
        )

    def test_course_roster_shows_each_student_type(self) -> None:
        """The roster shows each student's own level (polymorphism)."""
        report = CourseRosterReport(self.cs, self.enrollments)
        lines = report.generate().splitlines()
        self.assertEqual(
            lines[0], "Roster for CS101 - Introduction to Programming"
        )
        self.assertEqual(lines[2], "2 student(s)")
        self.assertIn("Alice Uwase", lines[3])
        self.assertIn("Graduate", lines[3])
        self.assertIn("Grade: 85.0", lines[3])
        self.assertIn("Ben Habimana", lines[4])
        self.assertIn("Undergraduate", lines[4])
        self.assertIn("Grade: -", lines[4])

    def test_empty_roster(self) -> None:
        """A course with no students says so."""
        report = CourseRosterReport(
            Course("PHY110", "General Physics"), self.enrollments
        )
        self.assertEqual(report.lines(), ["No students enrolled."])


if __name__ == "__main__":
    unittest.main()

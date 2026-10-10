"""Tests for the student classes and the student registry."""

import unittest

from student import GraduateStudent, StudentRegistry, UndergraduateStudent


class StudentTest(unittest.TestCase):
    """Validation, polymorphism, and magic methods of Student."""

    def test_name_is_trimmed(self) -> None:
        """Surrounding spaces are removed from the name."""
        student = UndergraduateStudent("S001", "  Alice Uwase  ")
        self.assertEqual(student.name, "Alice Uwase")

    def test_empty_name_is_rejected(self) -> None:
        """A blank name raises ValueError."""
        with self.assertRaises(ValueError):
            UndergraduateStudent("S001", "   ")

    def test_level_depends_on_student_type(self) -> None:
        """Each subclass supplies its own level."""
        self.assertEqual(
            UndergraduateStudent("S001", "Ana").level, "Undergraduate"
        )
        self.assertEqual(GraduateStudent("S002", "Ben").level, "Graduate")

    def test_create_builds_the_subclass_it_is_called_on(self) -> None:
        """The classmethod returns the calling subclass with a padded ID."""
        student = GraduateStudent.create(7, "Ana")
        self.assertIsInstance(student, GraduateStudent)
        self.assertEqual(student.id, "S007")

    def test_students_are_equal_by_id(self) -> None:
        """Two students with the same ID compare equal."""
        self.assertEqual(
            UndergraduateStudent("S001", "Ana"),
            UndergraduateStudent("S001", "Another Name"),
        )
        self.assertNotEqual(
            UndergraduateStudent("S001", "Ana"),
            UndergraduateStudent("S002", "Ana"),
        )

    def test_repr_shows_type_id_and_name(self) -> None:
        """__repr__ names the subclass and its key fields."""
        self.assertEqual(
            repr(GraduateStudent("S001", "Ana")),
            "GraduateStudent(id='S001', name='Ana')",
        )

    def test_details_cannot_be_changed_from_outside(self) -> None:
        """The details property returns a copy."""
        student = UndergraduateStudent("S001", "Ana", email="ana@example.com")
        student.details["email"] = "changed"
        self.assertEqual(student.details, {"email": "ana@example.com"})


class StudentRegistryTest(unittest.TestCase):
    """Registering and looking up students."""

    def setUp(self) -> None:
        """Start each test with an empty registry."""
        self.students = StudentRegistry()

    def test_ids_are_assigned_in_order(self) -> None:
        """Each new student gets the next ID."""
        first = self.students.add_student("Ana")
        second = self.students.add_student("Ben", GraduateStudent)
        self.assertEqual((first.id, second.id), ("S001", "S002"))
        self.assertIsInstance(second, GraduateStudent)

    def test_default_type_is_undergraduate(self) -> None:
        """Without a type, an undergraduate is created."""
        self.assertIsInstance(
            self.students.add_student("Ana"), UndergraduateStudent
        )

    def test_get_is_case_insensitive(self) -> None:
        """IDs can be looked up in any case."""
        student = self.students.add_student("Ana")
        self.assertIs(self.students.get("s001"), student)

    def test_get_unknown_id_returns_none(self) -> None:
        """An unknown ID returns None."""
        self.assertIsNone(self.students.get("S999"))


if __name__ == "__main__":
    unittest.main()

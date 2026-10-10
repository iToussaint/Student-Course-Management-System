"""End-to-end tests of the console menus, with scripted input."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import main


def run_session(*steps: tuple[str, ...]) -> str:
    """Run the app and return everything it printed.

    Args:
        *steps: The inputs for each menu action, typed in order.
    """
    inputs = [value for step in steps for value in step]
    output = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
        main()
    return output.getvalue()


class ConsoleAppTest(unittest.TestCase):
    """Whole user journeys through the menus."""

    def test_register_enroll_grade_and_report(self) -> None:
        """A student registers, enrolls, is graded, and views a summary."""
        output = run_session(
            ("1",),  # Student menu
            ("1", "Alice Uwase", "2"),  # Register as a graduate
            ("2", "S001", "CS101 math201 XX1 cs101"),  # Enroll
            ("0",),  # Back
            ("2",),  # Instructor menu
            ("4", "CS101", "S001", "abc", "120", "85"),  # Record grade
            ("5", "CS101"),  # Course average
            ("0",),  # Back
            ("1",),  # Student menu
            ("3", "S001"),  # View summary
            ("0", "0"),  # Back, Exit
        )
        self.assertIn(
            "Registered Alice Uwase (Graduate) with ID S001.", output
        )
        self.assertIn("Enrolled in: CS101, MATH201", output)
        self.assertIn("Unknown course code(s): XX1", output)
        self.assertIn("Grade must be a number.", output)
        self.assertIn("Grade must be between 0 and 100.", output)
        self.assertIn("Recorded 85.0 for Alice Uwase in CS101.", output)
        self.assertIn("Average grade for CS101: 85.0", output)
        self.assertIn("Summary for Alice Uwase (S001, Graduate)", output)
        self.assertIn("Average grade: 85.0", output)
        self.assertTrue(output.rstrip().endswith("Goodbye!"))

    def test_instructor_manages_roster(self) -> None:
        """An instructor adds, lists, and removes a student."""
        output = run_session(
            ("1", "1", "Ben Habimana", "1", "0"),  # Register undergraduate
            ("2",),  # Instructor menu
            ("2", "PHY110", "S001"),  # Add to roster
            ("2", "PHY110", "S001"),  # Add again
            ("1", "PHY110"),  # View roster
            ("3", "PHY110", "S001"),  # Remove
            ("3", "PHY110", "S001"),  # Remove again
            ("0", "0"),  # Back, Exit
        )
        self.assertIn("Added Ben Habimana to PHY110.", output)
        self.assertIn("Ben Habimana is already on the PHY110 roster.", output)
        self.assertIn("Undergraduate", output)
        self.assertIn("Removed Ben Habimana from PHY110.", output)
        self.assertIn("Ben Habimana is not on the PHY110 roster.", output)

    def test_invalid_input_is_handled(self) -> None:
        """Bad menu choices and unknown IDs or codes give clear messages."""
        output = run_session(
            ("9",),  # Invalid main menu option
            ("1",),  # Student menu
            ("1", "", "Cleo", "5", "1"),  # Empty name, bad type, then valid
            ("3", "S404"),  # Unknown student
            ("0",),  # Back
            ("2",),  # Instructor menu
            ("5", "BIO100"),  # Unknown course
            ("5", "CS101"),  # No grades yet
            ("0", "0"),  # Back, Exit
        )
        self.assertIn("Invalid option. Please try again.", output)
        self.assertIn("Input cannot be empty. Please try again.", output)
        self.assertIn("Invalid option. Please enter 1 or 2.", output)
        self.assertIn("No student found with ID S404.", output)
        self.assertIn("No course found with code BIO100.", output)
        self.assertIn("No grades recorded for CS101 yet.", output)

    def test_end_of_input_exits_cleanly(self) -> None:
        """Ctrl+D / Ctrl+Z (EOFError) ends the app without a traceback."""
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=EOFError),
            redirect_stdout(output),
        ):
            main()
        self.assertTrue(output.getvalue().rstrip().endswith("Goodbye!"))


if __name__ == "__main__":
    unittest.main()

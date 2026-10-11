# Student Course Management System

A console application for managing students, courses, enrollments, and
grades, built with Python fundamentals, modular design, and object-oriented
programming.

## Features

**Students can:**

- Register as an undergraduate or graduate student (an ID such as `S001` is assigned)
- Enroll in one or more courses at once (e.g. `CS101 MATH201`)
- View a summary of their courses, grades, and average grade

**Instructors can:**

- View a course roster with each student's level and grade
- Add students to, or remove them from, a course roster
- Record a grade (0–100) for an enrolled student
- View the average grade for a course

Data is kept in memory while the program runs.

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management

## Setup

```bash
# Create the virtual environment with venv (Poetry is configured to use .venv in the project)
python -m venv .venv

# Install dependencies into .venv
poetry install

# Activate the virtual environment
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

## Run

```bash
python main.py
```

## Project structure

```text
.
├── main.py          # Console menus and input/output only
├── student.py       # Student class hierarchy and student registry
├── course.py        # Course class and course catalogue
├── enrollment.py    # Enrollment class, enrolling, rosters, averages
├── report.py        # Abstract Report class and concrete reports
└── pyproject.toml   # Project metadata, dependencies, lint settings
```

## Design

### Data structures

| Structure | Used for |
|---|---|
| List | `students`, `courses`: the collections in creation order |
| Dictionary | `students_by_id`, `courses_by_code`: fast lookup by ID or code |
| Set | `enrollments`: each student/course pair can appear only once |

### Classes

```text
Student (ABC)                Course          Enrollment          Report (ABC)
├── UndergraduateStudent                     student + course     ├── StudentSummaryReport
└── GraduateStudent                          + grade              └── CourseRosterReport
```

- **Encapsulation:** attributes are private (`_name`, `_grade`, ...) and exposed
  through `@property`. IDs and codes are read-only; `name` and `grade` have
  setters that validate their values.
- **Inheritance and polymorphism:** each student type implements the abstract
  `level` property, and reports display whichever type they are given. Any
  `Report` subclass can be printed with the same `generate()` call.
- **Abstraction:** `Report` defines the layout in `generate()` and leaves the
  `title` and `lines()` to each subclass.
- **Magic methods:** `__repr__` for readable debugging output, `__eq__` and
  `__hash__` so objects compare by ID/code and work in sets.
- **Class and static methods:** `Student.register()` creates and stores a
  student of whichever subclass it is called on; `Enrollment.is_valid_grade()`
  and `Report.format_grade()` are helpers that need no instance.

### Functions

`add_student(name, student_type, **details)`, `enroll_student(student, *courses)`,
and `calculate_average(*scores)` use `*args` / `**kwargs` so they accept any
number of courses, scores, or extra student details.

## Sample session

```text
# Student menu -> Register
Enter your full name: Alice Uwase
Student type - 1. Undergraduate  2. Graduate: 2
Registered Alice Uwase (Graduate) with ID S001.

# Student menu -> Enroll in courses
Enter student ID: S001
Enter course code(s), separated by spaces: CS101 MATH201
Enrolled in: CS101, MATH201

# Instructor menu -> Record grade
Enter course code: CS101
Enter student ID: S001
Enter grade (0-100): 85
Recorded 85.0 for Alice Uwase in CS101.

# Student menu -> View summary
Enter student ID: S001

Summary for Alice Uwase (S001, Graduate)
----------------------------------------
Courses enrolled: 2
  CS101    Introduction to Programming    Grade: 85.0
  MATH201  Linear Algebra                 Grade: -
Average grade: 85.0
```

## Code style

The code follows PEP 8 (79-character lines) with Google-style docstrings.
Lint settings are in `pyproject.toml` under `[tool.ruff]`; the VS Code Ruff
extension applies them automatically.

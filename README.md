# Class Attendance Tracker

## Purpose and Benefits

The Class Attendance Tracker is a console-based application designed to help teachers, instructors, and educational administrators efficiently manage student attendance records. This tool addresses the common challenge of tracking student presence in educational settings without requiring complex software or web applications.

### How It Helps People

- **Teachers and Instructors**: Simplifies the daily task of recording which students are present or absent, saving valuable classroom time and reducing paperwork.

- **Educational Administrators**: Provides a reliable system for maintaining attendance records that can be used for compliance reporting and identifying attendance patterns.

- **Students**: Ensures fair and accurate attendance recording, which is often tied to course completion requirements or participation grades.

- **Small Educational Settings**: Offers a lightweight solution for schools, tutoring centers, or training programs that don't need or can't afford complex attendance systems.

### Key Benefits

- **Simplicity**: Easy-to-use text-based interface that requires minimal training
- **Reliability**: Secure SQLite database ensures attendance data is never lost
- **Flexibility**: Works with any class size and allows historical record keeping
- **Accessibility**: Runs on any computer with Python installed, no internet required
- **Reporting**: Export capabilities for attendance analysis and record-keeping

## Project Structure

This project follows a proper Python package structure:

```
attendance_tracker/
├── __init__.py         # Main package initialization
├── models/             # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py         # Database connection setup
│   ├── student.py      # Student model
│   └── attendance.py   # Attendance model
├── cli/                # Command-line interface
│   ├── __init__.py
│   └── commands.py     # CLI commands implementation
└── utils/              # Utility functions
    ├── __init__.py
    └── helpers.py      # Helper functions
```

## Setup and Installation

1. Make sure you have Python 3.8+ installed
2. Install pipenv: `pip install pipenv`
3. Clone this repository
4. Run the setup script: `./setup.sh`
5. Activate the virtual environment: `pipenv shell`
6. Run the application: `python run.py`
7. To migrate existing data: `python migrate.py`

## Options and Usage

### 1. Add Student
**Usage:** Enter a student's name when prompted.
- Names must contain only letters and spaces
- Each student must have a unique name
- Example: `John Smith`

### 2. Mark Attendance
**Usage:** Follow the prompts to mark a student's attendance.
1. Select a student by entering their ID number
2. Enter a date in YYYY-MM-DD format (or leave blank for today)
3. Enter status as "present" or "absent"
- Example date: `2023-05-30`
- Future dates are not allowed

### 3. View Attendance Records
**Usage:** Simply select this option to view all attendance records.
- Records are displayed by student
- For each student, all attendance dates and statuses are shown
- A summary of total records is displayed at the end

### 4. List Students
**Usage:** Select this option to see all students in the roster.
- Shows each student's ID and name
- Displays the total number of students at the end

### 5. Database Check
**Usage:** Select this option to perform a diagnostic check.
- Shows the number of students in the database
- Lists all student IDs and names
- Shows the number of attendance records
- Displays detailed attendance information
- Shows the database file location

### 6. Mark All Students Present
**Usage:** Mark all students present for a specific date.
1. Enter a date in YYYY-MM-DD format (or leave blank for today)
- The system will mark all students as present for that date
- Students who already have attendance recorded for that date will be skipped
- A summary shows how many students were marked and how many were skipped

### 7. Export to CSV
**Usage:** Select this option to export attendance data to a CSV file.
- Creates a file named "attendance_export.csv" in the application directory
- The file contains columns for Student, Date, and Status
- Can be opened in Excel, Google Sheets, or any spreadsheet application
- Example: `Student,Date,Status`
          `ann,2025-05-27,present`

### 8. View Database Tables
**Usage:** Select this option to see the raw database contents.
- Shows all tables in the database
- Displays column names for each table
- Lists all rows in each table
- Useful for understanding the database structure or troubleshooting

### 9. Exit
**Usage:** Select this option to close the application.

## Technical Details

- **SQLAlchemy ORM**: Used for database operations with proper models and relationships
- **Virtual Environment**: Managed with Pipenv for dependency isolation
- **Package Structure**: Follows Python best practices with proper module organization
- **Data Types**: Uses lists, dictionaries, and tuples for data manipulation
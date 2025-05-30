import sqlite3
import os
from datetime import datetime

# ---------- Database Setup ----------
def initialize_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            status TEXT,
            UNIQUE(student_id, date),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')

    conn.commit()
    conn.close()

# ---------- List Students ----------
def list_students():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM students ORDER BY name ASC")
    students = cursor.fetchall()
    if not students:
        print("No students found.")
    else:
        print("\nStudent List:")
        for sid, name in students:
            print(f"{sid}. {name}")
            
        # Show total count
        print(f"\nTotal students: {len(students)}")
    conn.close()

# ---------- Add Student ----------
def add_student():
    name = input("Enter the student's name: ").strip()

    if not all(part.isalpha() for part in name.split()):
        print("Invalid name. Use alphabetic characters and spaces only.")
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Student '{name}' added.")
    except sqlite3.IntegrityError:
        print("This student already exists.")
    finally:
        conn.close()

# ---------- Mark Attendance ----------
def mark_attendance():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found. Add some first.")
        conn.close()
        return

    print("\nStudents:")
    for student in students:
        print(f"{student[0]}. {student[1]}")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid ID. Use a number.")
        conn.close()
        return

    if student_id not in [s[0] for s in students]:
        print("Student ID not found.")
        conn.close()
        return

    date_input = input("Enter date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_input:
        attendance_date = datetime.now().date()
    else:
        try:
            attendance_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            if attendance_date > datetime.now().date():
                print("Date can't be in the future.")
                conn.close()
                return
        except ValueError:
            print("Invalid date format.")
            conn.close()
            return

    status = input("Status (present/absent): ").lower()
    if status not in ("present", "absent"):
        print("Invalid status. Use 'present' or 'absent'.")
        conn.close()
        return

    try:
        cursor.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
            (student_id, str(attendance_date), status)
        )
        conn.commit()
        print("Attendance marked.")
    except sqlite3.IntegrityError:
        print("Attendance already recorded for this date.")
    finally:
        conn.close()

# ---------- View Attendance Records ----------
def view_attendance():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    print("\n===== ATTENDANCE RECORDS =====\n")
    
    # Get list of all students
    cursor.execute("SELECT id, name FROM students ORDER BY name")
    students = cursor.fetchall()
    
    if not students:
        print("No students in database.")
        conn.close()
        return
    
    # For each student, show their attendance
    for student_id, student_name in students:
        print(f"Student: {student_name} (ID: {student_id})")
        
        cursor.execute("""
            SELECT date, status FROM attendance 
            WHERE student_id = ? 
            ORDER BY date
        """, (student_id,))
        
        records = cursor.fetchall()
        
        if records:
            print("  Date       | Status")
            print("  -----------|--------")
            for date, status in records:
                print(f"  {date} | {status}")
        else:
            print("  No attendance records")
        
        print("")  # Empty line between students
    
    # Show summary
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_records = cursor.fetchone()[0]
    print(f"Total attendance records: {total_records}")
    
    conn.close()

# ---------- Check Database ----------
def check_database():
    print("\n--- Database Check ---")
    
    # Check if database file exists
    if not os.path.exists("attendance.db"):
        print("Database file doesn't exist yet!")
        return
        
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    # Check students table
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    print(f"Students in database: {student_count}")
    
    if student_count > 0:
        print("\nStudent records:")
        cursor.execute("SELECT id, name FROM students")
        for student in cursor.fetchall():
            print(f"  ID: {student[0]}, Name: {student[1]}")
    
    # Check attendance table
    cursor.execute("SELECT COUNT(*) FROM attendance")
    attendance_count = cursor.fetchone()[0]
    print(f"\nAttendance records in database: {attendance_count}")
    
    if attendance_count > 0:
        print("\nAttendance details:")
        cursor.execute("""
            SELECT students.name, attendance.date, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.id
        """)
        for record in cursor.fetchall():
            print(f"  {record[0]} on {record[1]}: {record[2]}")
    
    # Show file location
    db_path = os.path.abspath("attendance.db")
    print(f"\nDatabase location: {db_path}")
    
    conn.close()

# ---------- Mark All Students Present ----------
def mark_all_present():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    # Check if there are any students
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    
    if student_count == 0:
        print("No students found. Add some first.")
        conn.close()
        return
    
    # Get date
    date_input = input("Enter date for all students (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_input:
        attendance_date = datetime.now().date()
    else:
        try:
            attendance_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            if attendance_date > datetime.now().date():
                print("Date can't be in the future.")
                conn.close()
                return
        except ValueError:
            print("Invalid date format.")
            conn.close()
            return
    
    # Get all student IDs
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    
    # Mark all students present
    marked_count = 0
    skipped_count = 0
    
    for student_id, student_name in students:
        try:
            cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                (student_id, str(attendance_date), "present")
            )
            marked_count += 1
        except sqlite3.IntegrityError:
            # Student already has attendance for this date
            skipped_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\nMarked {marked_count} students present for {attendance_date}")
    if skipped_count > 0:
        print(f"Skipped {skipped_count} students who already had attendance recorded for this date")

# ---------- Export to CSV ----------
def export_to_csv():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT students.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        ORDER BY students.name, attendance.date
    """)
    
    records = cursor.fetchall()
    conn.close()
    
    if not records:
        print("No attendance records to export.")
        return
    
    with open("attendance_export.csv", "w") as f:
        f.write("Student,Date,Status\n")
        for name, date, status in records:
            f.write(f"{name},{date},{status}\n")
    
    print(f"Attendance data exported to {os.path.abspath('attendance_export.csv')}")

# ---------- View Database Tables ----------
def view_database_tables():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\n=== TABLE: {table_name} ===")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Print column headers
        header = " | ".join(columns)
        print(header)
        print("-" * len(header))
        
        # Get and print all rows
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(" | ".join(str(row[column]) for column in range(len(columns))))
    
    conn.close()

# ---------- Main Menu ----------
def menu():
    initialize_db()
    print("Welcome to the Class Attendance Tracker!")
    while True:
        print("\n--- Main Menu ---")
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. View Attendance Records")
        print("4. List Students")
        print("5. Database Check")
        print("6. Mark All Students Present")
        print("7. Export to CSV")
        print("8. View Database Tables")
        print("9. Exit")
        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            mark_attendance()
        elif choice == '3':
            view_attendance()
        elif choice == '4':
            list_students()
        elif choice == '5':
            check_database()
        elif choice == '6':
            mark_all_present()
        elif choice == '7':
            export_to_csv()
        elif choice == '8':
            view_database_tables()
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# ---------- Run the App ----------
if __name__ == "__main__":
    menu()
import sqlite3
from datetime import datetime

def mark_all_students_present_with_exceptions(date_str, absent_student_ids):
    """
    Mark all students present for a specific date, except for specified students who will be marked absent.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        absent_student_ids: List of student IDs to mark as absent
    """
    conn = sqlite3.connect("../attendance.db")
    cursor = conn.cursor()
    
    # Validate date format
    try:
        attendance_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY format.")
        conn.close()
        return
    
    # Get all student IDs
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    
    if not students:
        print("No students found in the database.")
        conn.close()
        return
    
    # First, delete any existing attendance records for this date
    cursor.execute("DELETE FROM attendance WHERE date = ?", (attendance_date,))
    
    # Mark attendance for all students
    present_count = 0
    absent_count = 0
    
    for student_id, student_name in students:
        status = "absent" if student_id in absent_student_ids else "present"
        
        cursor.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
            (student_id, attendance_date, status)
        )
        
        if status == "present":
            present_count += 1
        else:
            absent_count += 1
            print(f"Marked {student_name} (ID: {student_id}) as absent")
    
    conn.commit()
    conn.close()
    
    print(f"\nAttendance for {date_str} (stored as {attendance_date}):")
    print(f"- {present_count} students marked present")
    print(f"- {absent_count} students marked absent")

# Mark all students present for 25/05/2025, except for two students (IDs 1 and 3)
# who will be marked absent
mark_all_students_present_with_exceptions("25/05/2025", [1, 3])
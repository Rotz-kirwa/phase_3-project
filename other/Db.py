import sqlite3
import os

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

if __name__ == "__main__":
    check_database()
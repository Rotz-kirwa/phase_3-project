import sqlite3

def create_attendance_view():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    # Create a view that joins students and attendance tables
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS attendance_with_names AS
    SELECT 
        a.id as attendance_id,
        a.student_id,
        s.name as student_name,
        a.date,
        a.status
    FROM attendance a
    JOIN students s ON a.student_id = s.id
    """)
    
    conn.commit()
    conn.close()
    
    print("Created 'attendance_with_names' view in the database.")
    print("You can now see student names alongside attendance records in your SQLite browser.")

if __name__ == "__main__":
    create_attendance_view()
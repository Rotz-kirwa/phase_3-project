import sqlite3
import os
from attendance_tracker.models import Session, Base, engine, Student, Attendance

def migrate_data():
    """Migrate data from old SQLite database to new SQLAlchemy structure."""
    # Initialize the new database
    Base.metadata.create_all(engine)
    
    # Connect to the old database
    old_conn = sqlite3.connect("attendance.db")
    old_cursor = old_conn.cursor()
    
    # Create a session for the new database
    session = Session()
    
    try:
        # Migrate students
        print("Migrating students...")
        old_cursor.execute("SELECT id, name FROM students")
        students = old_cursor.fetchall()
        
        for student_id, name in students:
            # Check if student already exists
            existing = session.query(Student).filter_by(id=student_id).first()
            if not existing:
                student = Student(id=student_id, name=name)
                session.add(student)
        
        session.commit()
        print(f"Migrated {len(students)} students.")
        
        # Migrate attendance records
        print("Migrating attendance records...")
        old_cursor.execute("SELECT id, student_id, date, status FROM attendance")
        records = old_cursor.fetchall()
        
        for record_id, student_id, date, status in records:
            # Check if record already exists
            existing = session.query(Attendance).filter_by(id=record_id).first()
            if not existing:
                attendance = Attendance(
                    id=record_id,
                    student_id=student_id,
                    date=date,
                    status=status
                )
                session.add(attendance)
        
        session.commit()
        print(f"Migrated {len(records)} attendance records.")
        
        print("Migration complete!")
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {e}")
    finally:
        # Close connections
        old_conn.close()
        session.close()

if __name__ == "__main__":
    migrate_data()
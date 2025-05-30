import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from ..models import Session, Base, engine, Student, Attendance
from ..utils import validate_date, format_date, validate_name

def initialize_db():
    """Initialize the database and create tables if they don't exist."""
    Base.metadata.create_all(engine)
    print("Database initialized.")

def add_student():
    """Add a new student to the roster."""
    name = input("Enter the student's name: ").strip()
    
    valid, error = validate_name(name)
    if not valid:
        print(error)
        return
    
    session = Session()
    try:
        student = Student(name=name)
        session.add(student)
        session.commit()
        print(f"Student '{name}' added.")
    except IntegrityError:
        session.rollback()
        print("This student already exists.")
    finally:
        session.close()

def list_students():
    """List all students in the roster."""
    session = Session()
    students = session.query(Student).order_by(Student.name).all()
    
    if not students:
        print("No students found.")
    else:
        print("\nStudent List:")
        for student in students:
            print(f"{student.id}. {student.name}")
        print(f"\nTotal students: {len(students)}")
    
    session.close()

def mark_attendance():
    """Mark attendance for a student on a specific date."""
    session = Session()
    students = session.query(Student).all()
    
    if not students:
        print("No students found. Add some first.")
        session.close()
        return
    
    print("\nStudents:")
    for student in students:
        print(f"{student.id}. {student.name}")
    
    try:
        student_id = int(input("Enter student ID: "))
        student = session.query(Student).filter_by(id=student_id).first()
        if not student:
            print("Student ID not found.")
            session.close()
            return
    except ValueError:
        print("Invalid ID. Use a number.")
        session.close()
        return
    
    date_input = input("Enter date (YYYY-MM-DD) [leave blank for today]: ").strip()
    date_obj, error = validate_date(date_input)
    if error:
        print(error)
        session.close()
        return
    
    status = input("Status (present/absent): ").lower()
    if status not in ("present", "absent"):
        print("Invalid status. Use 'present' or 'absent'.")
        session.close()
        return
    
    try:
        # Check if record already exists
        existing = session.query(Attendance).filter_by(
            student_id=student_id, 
            date=format_date(date_obj)
        ).first()
        
        if existing:
            print("Attendance already recorded for this date.")
            session.close()
            return
            
        attendance = Attendance(
            student_id=student_id,
            date=format_date(date_obj),
            status=status
        )
        session.add(attendance)
        session.commit()
        print("Attendance marked.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

def view_attendance():
    """View attendance records for all students."""
    session = Session()
    students = session.query(Student).order_by(Student.name).all()
    
    if not students:
        print("No students in database.")
        session.close()
        return
    
    print("\n===== ATTENDANCE RECORDS =====\n")
    
    total_records = 0
    for student in students:
        print(f"Student: {student.name} (ID: {student.id})")
        
        attendance_records = session.query(Attendance).filter_by(student_id=student.id).order_by(Attendance.date).all()
        
        if attendance_records:
            print("  Date       | Status")
            print("  -----------|--------")
            for record in attendance_records:
                print(f"  {record.date} | {record.status}")
            total_records += len(attendance_records)
        else:
            print("  No attendance records")
        
        print("")  # Empty line between students
    
    print(f"Total attendance records: {total_records}")
    session.close()

def mark_all_present():
    """Mark all students present for a specific date."""
    session = Session()
    students = session.query(Student).all()
    
    if not students:
        print("No students found. Add some first.")
        session.close()
        return
    
    date_input = input("Enter date for all students (YYYY-MM-DD) [leave blank for today]: ").strip()
    date_obj, error = validate_date(date_input)
    if error:
        print(error)
        session.close()
        return
    
    date_str = format_date(date_obj)
    
    # Delete existing records for this date
    session.query(Attendance).filter_by(date=date_str).delete()
    
    marked_count = 0
    for student in students:
        attendance = Attendance(
            student_id=student.id,
            date=date_str,
            status="present"
        )
        session.add(attendance)
        marked_count += 1
    
    session.commit()
    session.close()
    
    print(f"\nMarked {marked_count} students present for {date_str}")

def export_to_csv():
    """Export attendance data to a CSV file."""
    session = Session()
    
    # Get all attendance records with student names
    records = session.query(
        Student.name,
        Attendance.date,
        Attendance.status
    ).join(
        Attendance, Student.id == Attendance.student_id
    ).order_by(
        Student.name, Attendance.date
    ).all()
    
    session.close()
    
    if not records:
        print("No attendance records to export.")
        return
    
    with open("attendance_export.csv", "w") as f:
        f.write("Student,Date,Status\n")
        for name, date, status in records:
            f.write(f"{name},{date},{status}\n")
    
    print(f"Attendance data exported to {os.path.abspath('attendance_export.csv')}")

def view_database_tables():
    """View the raw database tables."""
    session = Session()
    
    # Students table
    students = session.query(Student).all()
    print("\n=== TABLE: students ===")
    if students:
        print("id | name")
        print("---|-----")
        for student in students:
            print(f"{student.id} | {student.name}")
    else:
        print("No records")
    
    # Attendance table
    attendance_records = session.query(Attendance).all()
    print("\n=== TABLE: attendance ===")
    if attendance_records:
        print("id | student_id | date | status")
        print("---|------------|------|-------")
        for record in attendance_records:
            print(f"{record.id} | {record.student_id} | {record.date} | {record.status}")
    else:
        print("No records")
    
    session.close()

def check_database():
    """Check the database for diagnostic purposes."""
    session = Session()
    
    print("\n--- Database Check ---")
    
    # Check students table
    student_count = session.query(Student).count()
    print(f"Students in database: {student_count}")
    
    if student_count > 0:
        print("\nStudent records:")
        students = session.query(Student).all()
        for student in students:
            print(f"  ID: {student.id}, Name: {student.name}")
    
    # Check attendance table
    attendance_count = session.query(Attendance).count()
    print(f"\nAttendance records in database: {attendance_count}")
    
    if attendance_count > 0:
        print("\nAttendance details:")
        records = session.query(
            Student.name, Attendance.date, Attendance.status
        ).join(
            Attendance, Student.id == Attendance.student_id
        ).all()
        
        for name, date, status in records:
            print(f"  {name} on {date}: {status}")
    
    # Show file location
    db_path = os.path.abspath("attendance.db")
    print(f"\nDatabase location: {db_path}")
    
    session.close()
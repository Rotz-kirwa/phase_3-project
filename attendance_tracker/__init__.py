from .cli import (
    initialize_db, add_student, list_students, mark_attendance,
    view_attendance, mark_all_present, export_to_csv,
    view_database_tables, check_database
)

def main():
    """Main function to run the attendance tracker."""
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
        
        input("\nPress Enter to continue...")
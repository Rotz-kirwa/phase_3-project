from datetime import datetime

def validate_date(date_str, allow_empty=True):
    """Validate date string format and return datetime object."""
    if allow_empty and not date_str:
        return datetime.now().date(), None
    
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_obj > datetime.now().date():
            return None, "Date can't be in the future."
        return date_obj, None
    except ValueError:
        return None, "Invalid date format. Please use YYYY-MM-DD."

def format_date(date_obj):
    """Format date object to string."""
    return date_obj.strftime("%Y-%m-%d")

def validate_name(name):
    """Validate student name."""
    if not name or not all(c.isalpha() or c.isspace() for c in name):
        return False, "Invalid name. Use alphabetic characters and spaces only."
    return True, None
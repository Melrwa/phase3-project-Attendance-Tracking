from datetime import datetime

def get_current_time():
    """Returns the current date and time."""
    return datetime.now()

def format_time(dt):
    """Formats the datetime object into a readable string."""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def validate_id(user_id):
    """Validates if the user_id is an integer."""
    try:
        return int(user_id)
    except ValueError:
        return None


from datetime import datetime
from lib.db.models import  Student, Staff, Visitor

def get_current_time():
    """Returns the current datetime."""
    return datetime.now()

def format_time(time):
    """Formats a datetime object as a readable string."""
    return time.strftime('%Y-%m-%d %H:%M:%S')

def validate_id(user_id):
    """Validates that the user_id is a positive integer."""
    try:
        user_id = int(user_id)
        if user_id > 0:
            return user_id
        else:
            return None
    except ValueError:
        return None
def validate_user_existence(user_id, user_type, session):
    if user_type == 'student':
        return session.query(Student).filter_by(id=user_id).first() is not None
    elif user_type == 'staff':
        return session.query(Staff).filter_by(id=user_id).first() is not None
    elif user_type == 'visitor':
        return session.query(Visitor).filter_by(id=user_id).first() is not None
    return False

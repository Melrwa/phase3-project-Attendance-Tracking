from lib.db.models import Session, Attendance
from datetime import datetime, timedelta

def generate_daily_report():
    """Generates a report of today's attendance."""
    session = Session()
    today = datetime.now().date()
    attendances = session.query(Attendance).filter(Attendance.date == today).all()
    for record in attendances:
        print(f"User ID: {record.user_id}, Clock In: {record.clock_in_time}, Clock Out: {record.clock_out_time}")

def generate_weekly_report():
    """Generates a report for the past 7 days."""
    session = Session()
    seven_days_ago = datetime.now() - timedelta(days=7)
    attendances = session.query(Attendance).filter(Attendance.date >= seven_days_ago).all()
    for record in attendances:
        print(f"User ID: {record.user_id}, Clock In: {record.clock_in_time}, Clock Out: {record.clock_out_time}")

if __name__ == '__main__':
    generate_daily_report()
    generate_weekly_report()

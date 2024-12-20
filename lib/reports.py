import os
import click
from datetime import datetime, timedelta
from lib.db.models import Session, Student, Staff, Visitor, Attendance, Course

def ensure_report_directory():
    """Ensures that the reports directory exists."""
    os.makedirs('reports', exist_ok=True)  # Create the 'reports' directory if it does not exist

def write_to_file(filename, content):
    """
    Writes the content to a markdown file in the 'reports' directory.
    
    Args:
        filename (str): Name of the file to be created.
        content (str): Content to be written into the file.
    """
    ensure_report_directory()  # Ensure the directory exists
    with open(f'reports/{filename}', 'w') as file:  # Open the file in write mode
        file.write(content)  # Write the content to the file

def generate_daily_report():
    """
    Generates a daily report summarizing activities for courses, staff, students, and visitors.
    The report includes attendance and role information.
    """
    session = Session()  # Start a database session
    start_of_day = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)  # Define the start of the day

    # Initialize report content
    content = "# Daily Report\n\n"

    # Add section for courses clocked into during the day
    content += "## Courses Clocked Into Within a Day\n\n"
    courses = session.query(Course).all()  # Fetch all courses from the database
    for course in courses:
        # Query attendance records for the course on the same day
        course_attendance = session.query(Attendance).join(Student).filter(
            Student.course_id == course.id,
            Attendance.student_id == Student.id,
            Attendance.clock_in_time >= start_of_day
        ).all()
        if course_attendance:  # Only include courses with attendance
            content += f'### {course.name}\n\n'
            for attendance in course_attendance:
                student = session.query(Student).filter_by(id=attendance.student_id).first()
                if student:  # Ensure the student exists
                    # Format clock-in and clock-out times
                    clock_in = attendance.clock_in_time.strftime('%Y-%m-%d %H:%M:%S')
                    clock_out = attendance.clock_out_time.strftime('%Y-%m-%d %H:%M:%S') if attendance.clock_out_time else ''
                    content += f'- **{student.name}** — Clocked In: {clock_in}, Clocked Out: {clock_out}\n'

    # Add section for staff attendance
    content += "\n## Staff Clocked In Within a Day\n\n"
    staff_attendance = session.query(Attendance).filter(
        Attendance.staff_id != None,
        Attendance.clock_in_time >= start_of_day
    ).all()
    for attendance in staff_attendance:
        staff = session.query(Staff).filter_by(id=attendance.staff_id).first()
        if staff:  # Ensure the staff member exists
            # Format clock-in and clock-out times
            clock_in = attendance.clock_in_time.strftime('%Y-%m-%d %H:%M:%S')
            clock_out = attendance.clock_out_time.strftime('%Y-%m-%d %H:%M:%S') if attendance.clock_out_time else ''
            content += f'- **{staff.name}** — Clocked In: {clock_in}, Clocked Out: {clock_out}\n'

    # Add section for visitor attendance
    content += "\n## Visitors Who Visited Within a Day\n\n"
    visitor_attendance = session.query(Attendance).filter(
        Attendance.visitor_id != None,
        Attendance.clock_in_time >= start_of_day
    ).all()
    for attendance in visitor_attendance:
        visitor = session.query(Visitor).filter_by(id=attendance.visitor_id).first()
        if visitor:  # Ensure the visitor exists
            # Format clock-in and clock-out times
            clock_in = attendance.clock_in_time.strftime('%Y-%m-%d %H:%M:%S')
            clock_out = attendance.clock_out_time.strftime('%Y-%m-%d %H:%M:%S') if attendance.clock_out_time else ''
            content += f'- **{visitor.name}** — Reason: {visitor.reason} — Clock In: {clock_in}, Clock Out: {clock_out}\n'

    # Add section for all students and their courses
    content += "\n## All Students and Their Courses\n\n"
    students = session.query(Student).all()  # Fetch all students
    for student in students:
        course = session.query(Course).filter_by(id=student.course_id).first()
        course_name = course.name if course else 'No Course Assigned'  # Handle students without assigned courses
        content += f'- **{student.name}** — Course: {course_name}\n'

    # Add section for all staff and their roles
    content += "\n## All Staff and Their Roles\n\n"
    staff_members = session.query(Staff).all()  # Fetch all staff members
    for staff in staff_members:
        content += f'- **{staff.name}** — Role: {staff.role}\n'

    # Write the generated content to a file
    write_to_file('daily_report.md', content)

def generate_weekly_report():
    """
    Generates a weekly report summarizing activities for students, staff, and visitors.
    The report includes aggregated clock-in counts for the week.
    """
    session = Session()  # Start a database session
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())  # Determine the start of the current week

    # Initialize report content
    content = "# Weekly Report\n\n"

    # Add section for student clock-ins during the week
    content += "## Students Who Clocked In During the Week\n\n"
    student_attendance = session.query(Attendance).filter(
        Attendance.student_id != None,
        Attendance.clock_in_time >= start_of_week
    ).all()
    student_clock_ins = {}
    for attendance in student_attendance:
        student = session.query(Student).filter_by(id=attendance.student_id).first()
        if student:  # Ensure the student exists
            # Aggregate clock-in counts by student name
            student_clock_ins[student.name] = student_clock_ins.get(student.name, 0) + 1
    for student_name, clock_ins in student_clock_ins.items():
        content += f'- **{student_name}** — Clock-ins: {clock_ins}\n'

    # Add section for staff clock-ins during the week
    content += "\n## Staff Who Clocked In During the Week\n\n"
    staff_attendance = session.query(Attendance).filter(
        Attendance.staff_id != None,
        Attendance.clock_in_time >= start_of_week
    ).all()
    staff_clock_ins = {}
    for attendance in staff_attendance:
        staff = session.query(Staff).filter_by(id=attendance.staff_id).first()
        if staff:  # Ensure the staff member exists
            # Aggregate clock-in counts by staff name
            staff_clock_ins[staff.name] = staff_clock_ins.get(staff.name, 0) + 1
    for staff_name, clock_ins in staff_clock_ins.items():
        content += f'- **{staff_name}** — Clock-ins: {clock_ins}\n'

    # Add section for visitor clock-ins during the week
    content += "\n## Visitors Who Visited During the Week\n\n"
    visitor_attendance = session.query(Attendance).filter(
        Attendance.visitor_id != None,
        Attendance.clock_in_time >= start_of_week
    ).all()
    visitor_clock_ins = {}
    for attendance in visitor_attendance:
        visitor = session.query(Visitor).filter_by(id=attendance.visitor_id).first()
        if visitor:  # Ensure the visitor exists
            # Aggregate clock-in counts by visitor name
            visitor_clock_ins[visitor.name] = visitor_clock_ins.get(visitor.name, 0) + 1
    for visitor_name, clock_ins in visitor_clock_ins.items():
        content += f'- **{visitor_name}** — Clock-ins: {clock_ins}\n'

    # Write the generated content to a file
    write_to_file('weekly_report.md', content)

if __name__ == '__main__':
    # Generate and print daily and weekly reports
    print("Generating daily report...")
    generate_daily_report()
    print("Generating weekly report...")
    generate_weekly_report()

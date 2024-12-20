import click
from datetime import datetime, timedelta
from lib.db.models import Session, Student, Staff, Visitor, Attendance, Course
from lib.helpers import get_current_time, format_time, validate_id, validate_user_existence
from lib.reports import generate_daily_report, generate_weekly_report



# Check for active clock-in
def has_active_clock_in(user_id, user_type, session):
    if user_type == 'student':
        return session.query(Attendance).filter_by(student_id=user_id, clock_out_time=None).first()
    elif user_type == 'staff':
        return session.query(Attendance).filter_by(staff_id=user_id, clock_out_time=None).first()
    elif user_type == 'visitor':
        return session.query(Attendance).filter_by(visitor_id=user_id, clock_out_time=None).first()
    return None

# Check for last clock-in within 12 hours
def can_clock_in(user_id, user_type, session):
    twelve_hours_ago = get_current_time() - timedelta(hours=12)
    if user_type == 'student':
        return not session.query(Attendance).filter(Attendance.student_id == user_id, Attendance.clock_in_time > twelve_hours_ago).first()
    elif user_type == 'staff':
        return not session.query(Attendance).filter(Attendance.staff_id == user_id, Attendance.clock_in_time > twelve_hours_ago).first()
    elif user_type == 'visitor':
        return not session.query(Attendance).filter(Attendance.visitor_id == user_id, Attendance.clock_in_time > twelve_hours_ago).first()
    return False

# Clock-in functionality
def clock_in(user_id, user_type):
    session = Session()
    user_id = validate_id(user_id)
    if not user_id or not validate_user_existence(user_id, user_type, session):
        click.echo('*** Invalid ID or user not found. ***')
        return

    # Check for active clock-in
    if has_active_clock_in(user_id, user_type, session):
        click.echo('*** You already have an active clock-in. Please clock out before clocking in again. ***')
        return

    # Check if clock-in is allowed within 12 hours
    if not can_clock_in(user_id, user_type, session):
        click.echo('*** You can only clock in once every 12 hours. ***')
        return

    if user_type == 'student':
        student = session.query(Student).filter_by(id=user_id).first()
        if not student.course_id:
            click.echo('*** You are not assigned to any course. Please contact administration. ***')
            return
        
        course = session.query(Course).filter_by(id=student.course_id).first()
        click.echo(f'*** You are assigned to the course: {course.name} and course ID is {student.course_id}. ***')
        
        selected_course_id = click.prompt('Enter the course number to clock in', type=int)
        if selected_course_id != student.course_id:
            click.echo('*** You can only clock in to your assigned course. ***')
            return

    attendance = Attendance(clock_in_time=get_current_time())
    if user_type == 'student':
        attendance.student_id = user_id
    elif user_type == 'staff':
        attendance.staff_id = user_id
    elif user_type == 'visitor':
        attendance.visitor_id = user_id

    session.add(attendance)
    session.commit()
    click.echo(f"=== Clock-in Successful! ===\nRecorded at: {format_time(attendance.clock_in_time)}")

# Clock-out functionality
def clock_out(user_id, user_type):
    session = Session()
    user_id = validate_id(user_id)
    if not user_id or not validate_user_existence(user_id, user_type, session):
        click.echo('*** Invalid ID or user not found. ***')
        return

    attendance = has_active_clock_in(user_id, user_type, session)
    if attendance:
        attendance.clock_out_time = get_current_time()
        session.commit()
        click.echo(f"=== Clock-out Successful! ===\nRecorded at: {format_time(attendance.clock_out_time)}")
    else:
        click.echo('*** No active clock-in found. ***')

# Create new student
def create_student():
    click.echo("=== Create New Student ===")
    name = click.prompt('Enter student name')
    session = Session()
    courses = session.query(Course).all()
    click.echo('Please select a course:')
    for course in courses:
        click.echo(f'{course.id}. {course.name}')
    selected_course_id = click.prompt('Enter the course number', type=int)
    
    selected_course = session.query(Course).filter_by(id=selected_course_id).first()
    if selected_course:
        new_student = Student(name=name, course_id=selected_course.id)
        session.add(new_student)
        session.commit()
        click.echo(f"=== Success! ===\nStudent {name} created and assigned to {selected_course.name} course.")
    else:
        click.echo('*** Invalid course selection. ***')

# Create new staff
def create_staff():
    click.echo("=== Create New Staff ===")
    name = click.prompt('Enter staff name')
    role = click.prompt('Enter staff role')
    session = Session()
    new_staff = Staff(name=name, role=role)
    session.add(new_staff)
    session.commit()
    click.echo(f"=== Success! ===\nStaff {name} created with the role of {role}.")

# Create new visitor
def create_visitor():
    click.echo("=== Create New Visitor ===")
    name = click.prompt('Enter visitor name')
    reason = click.prompt('Enter visitor reason')
    session = Session()
    new_visitor = Visitor(name=name, reason=reason)
    session.add(new_visitor)
    session.commit()
    click.echo(f"=== Success! ===\nVisitor {name} created for the reason: {reason}.")

# Create Course functionality
def create_course():
    click.echo("=== Create New Course ===")
    session = Session()
    course_name = click.prompt('Enter course name')
    new_course = Course(name=course_name)
    session.add(new_course)
    session.commit()
    click.echo(f"=== Success! ===\nCourse \"{course_name}\" created successfully.")


# Delete a student
def delete_student():
    click.echo("=== Delete a Student ===")
    session = Session()
    students = session.query(Student).all()
    if not students:
        click.echo("*** No students found to delete. ***")
        return

    click.echo("Available Students:")
    for student in students:
        click.echo(f"ID: {student.id}, Name: {student.name}")

    student_id = click.prompt("Enter the student ID to delete", type=int)
    student_to_delete = session.query(Student).filter_by(id=student_id).first()

    if student_to_delete:
        session.delete(student_to_delete)
        session.commit()
        click.echo(f"=== Success! ===\nStudent with ID {student_id} deleted.")
    else:
        click.echo("*** Invalid student ID. ***")

# Delete a staff member
def delete_staff():
    click.echo("=== Delete a Staff Member ===")
    session = Session()
    staff_members = session.query(Staff).all()
    if not staff_members:
        click.echo("*** No staff members found to delete. ***")
        return

    click.echo("Available Staff Members:")
    for staff in staff_members:
        click.echo(f"ID: {staff.id}, Name: {staff.name}, Role: {staff.role}")

    staff_id = click.prompt("Enter the staff ID to delete", type=int)
    staff_to_delete = session.query(Staff).filter_by(id=staff_id).first()

    if staff_to_delete:
        session.delete(staff_to_delete)
        session.commit()
        click.echo(f"=== Success! ===\nStaff with ID {staff_id} deleted.")
    else:
        click.echo("*** Invalid staff ID. ***")

# Delete a visitor
def delete_visitor():
    click.echo("=== Delete a Visitor ===")
    session = Session()
    visitors = session.query(Visitor).all()
    if not visitors:
        click.echo("*** No visitors found to delete. ***")
        return

    click.echo("Available Visitors:")
    for visitor in visitors:
        click.echo(f"ID: {visitor.id}, Name: {visitor.name}, Reason: {visitor.reason}")

    visitor_id = click.prompt("Enter the visitor ID to delete", type=int)
    visitor_to_delete = session.query(Visitor).filter_by(id=visitor_id).first()

    if visitor_to_delete:
        session.delete(visitor_to_delete)
        session.commit()
        click.echo(f"=== Success! ===\nVisitor with ID {visitor_id} deleted.")
    else:
        click.echo("*** Invalid visitor ID. ***")

#Menu Display
def show_menu():
    click.echo("\n====================")
    click.echo("Attendance Tracking System")
    click.echo("====================")
    click.echo("1. Clock In")
    click.echo("2. Clock Out")
    click.echo("3. Create Student")
    click.echo("4. Create Staff")
    click.echo("5. Create Visitor")
    click.echo("6. Create Course")
    click.echo("7. Generate Daily Report")
    click.echo("8. Generate Weekly Report")
    click.echo("9. Delete Student")
    click.echo("10. Delete Staff")
    click.echo("11. Delete Visitor")
    click.echo("0. Exit")
    click.echo("====================")


# Handle menu choice
def handle_menu_choice(choice):
    menu_options = {
        '1': lambda: clock_in(click.prompt('Enter your ID'), click.prompt('Are you a student, staff, or visitor?', type=click.Choice(['student', 'staff', 'visitor']))),
        '2': lambda: clock_out(click.prompt('Enter your ID'), click.prompt('Are you a student, staff, or visitor?', type=click.Choice(['student', 'staff', 'visitor']))),
        '3': create_student,
        '4': create_staff,
        '5': create_visitor,
        '6': create_course,
        '7': generate_daily_report,
        '8': generate_weekly_report,
        '9': delete_student,
        '10': delete_staff,
        '11': delete_visitor,
    }


    if choice in menu_options:
        menu_options[choice]()
    elif choice == '0':
        click.echo("=== Exiting... Goodbye! ===")
        return False
    else:
        click.echo("*** Invalid choice. Please try again. ***")
    return True

@click.command()
def cli():
    while True:
        show_menu()
        choice = click.prompt('Please select an option')
        if not handle_menu_choice(choice):
            break

if __name__ == '__main__':
    cli()


import click
from lib.db.models import Session, Student, Staff, Visitor, Attendance
from lib.helpers import get_current_time, format_time, validate_id, validate_user_existence


# Clock-in functionality
def clock_in(user_id, user_type):
    session = Session()
    user_id = validate_id(user_id)
    if not user_id or not validate_user_existence(user_id, user_type, session):
        click.echo('Invalid ID or user not found.')
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
    click.echo(f'Clock-in recorded at {format_time(attendance.clock_in_time)}')

# Clock-out functionality
def clock_out(user_id, user_type):
    session = Session()
    user_id = validate_id(user_id)
    if not user_id or not validate_user_existence(user_id, user_type, session):
        click.echo('Invalid ID or user not found.')
        return

    attendance = None
    if user_type == 'student':
        attendance = session.query(Attendance).filter_by(student_id=user_id, clock_out_time=None).first()
    elif user_type == 'staff':
        attendance = session.query(Attendance).filter_by(staff_id=user_id, clock_out_time=None).first()
    elif user_type == 'visitor':
        attendance = session.query(Attendance).filter_by(visitor_id=user_id, clock_out_time=None).first()

    if attendance:
        attendance.clock_out_time = get_current_time()
        session.commit()
        click.echo(f'Clock-out recorded at {format_time(attendance.clock_out_time)}')
    else:
        click.echo('No active clock-in found.')

# Create new student
def create_student():
    name = click.prompt('Enter student name')
    course = click.prompt('Enter student course')
    session = Session()
    new_student = Student(name=name, course=course)
    session.add(new_student)
    session.commit()
    click.echo(f'Student {name} created.')

# Create new staff
def create_staff():
    name = click.prompt('Enter staff name')
    role = click.prompt('Enter staff role')
    session = Session()
    new_staff = Staff(name=name, role=role)
    session.add(new_staff)
    session.commit()
    click.echo(f'Staff {name} created.')

# Create new visitor
def create_visitor():
    name = click.prompt('Enter visitor name')
    reason = click.prompt('Enter visitor reason')
    session = Session()
    new_visitor = Visitor(name=name, reason=reason)
    session.add(new_visitor)
    session.commit()
    click.echo(f'Visitor {name} created.')

# Menu display
def show_menu():
    click.echo("Attendance Tracking System")
    click.echo("1. Clock In")
    click.echo("2. Clock Out")
    click.echo("3. Create Student")
    click.echo("4. Create Staff")
    click.echo("5. Create Visitor")
    click.echo("0. Exit")

# Handle menu choice
def handle_menu_choice(choice):
    menu_options = {
        '1': lambda: clock_in(click.prompt('Enter your ID'), click.prompt('Are you a student, staff, or visitor?', type=click.Choice(['student', 'staff', 'visitor']))),
        '2': lambda: clock_out(click.prompt('Enter your ID'), click.prompt('Are you a student, staff, or visitor?', type=click.Choice(['student', 'staff', 'visitor']))),
        '3': create_student,
        '4': create_staff,
        '5': create_visitor,
    }

    if choice in menu_options:
        menu_options[choice]()
    elif choice == '0':
        click.echo("Exiting... Goodbye!")
        return False
    else:
        click.echo("Invalid choice. Please try again.")
    return True

# Main CLI function
@click.command()
def cli():
    while True:
        show_menu()
        choice = click.prompt('Please select an option')
        if not handle_menu_choice(choice):
            break

if __name__ == '__main__':
    cli()
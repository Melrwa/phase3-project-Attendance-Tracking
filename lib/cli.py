import click
from lib.db.models import Session, Student, Staff, Attendance
from lib.helpers import get_current_time, format_time, validate_id

@click.group()
def cli():
    """Simple CLI for tracking student and staff attendance."""
    pass

@cli.command()
@click.option('--user_id', prompt='Enter your ID', help='Your unique user ID')
@click.option('--user_type', prompt='Are you a student or staff?', type=click.Choice(['student', 'staff']))
def clock_in(user_id, user_type):
    """Allows a student or staff to clock in."""
    session = Session()
    user_id = validate_id(user_id)
    if not user_id:
        click.echo('Invalid ID. Please enter a valid number.')
        return

    attendance = Attendance(user_id=user_id, user_type=user_type, clock_in_time=get_current_time())
    session.add(attendance)
    session.commit()
    click.echo(f'Clock-in recorded at {format_time(attendance.clock_in_time)}')

@cli.command()
@click.option('--user_id', prompt='Enter your ID', help='Your unique user ID')
def clock_out(user_id):
    """Allows a student or staff to clock out."""
    session = Session()
    user_id = validate_id(user_id)
    if not user_id:
        click.echo('Invalid ID. Please enter a valid number.')
        return

    attendance = session.query(Attendance).filter_by(user_id=user_id, clock_out_time=None).first()
    if attendance:
        attendance.clock_out_time = get_current_time()
        session.commit()
        click.echo(f'Clock-out recorded at {format_time(attendance.clock_out_time)}')
    else:
        click.echo('No active clock-in found.')

if __name__ == '__main__':
    cli()

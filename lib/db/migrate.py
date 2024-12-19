from sqlalchemy import create_engine

# Create Database Engine
engine = create_engine('sqlite:///db/attendance.db')

# Example: Add a new "email" column to the "students" table
# def add_email_to_students():
#     with engine.connect() as conn:
#         conn.execute('ALTER TABLE students ADD COLUMN email VARCHAR(255)')

# # # Example: Drop the "staff" table (optional, just for example)
# def drop_table_staff():
#     with engine.connect() as conn:
#         conn.execute('DROP TABLE IF EXISTS staff')

# def drop_table_students():
#     with engine.connect() as conn:
#         conn.execute('DROP TABLE IF EXISTS students')

# def drop_table_visitors():
#     with engine.connect() as conn:
#         conn.execute('DROP TABLE IF EXISTS visitors')

# def drop_table_attendance():
#     with engine.connect() as conn:
#         conn.execute('DROP TABLE IF EXISTS attendance')

# Run all migrations
def run_migrations():
    print("Running migrations...")
    # add_email_to_students()
    # drop_table_staff()
    # drop_table_visitors()
    # drop_table_students()
    # drop_table_attendance()
    # Add any new migrations here

if __name__ == '__main__':
    run_migrations()

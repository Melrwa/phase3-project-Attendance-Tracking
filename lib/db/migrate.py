from sqlalchemy import create_engine

# Create Database Engine
engine = create_engine('sqlite:///db/attendance.db')

# Example: Add a new "email" column to the "students" table
# def add_email_to_students():
#     with engine.connect() as conn:
#         conn.execute('ALTER TABLE students ADD COLUMN email VARCHAR(255)')

# # Example: Drop the "staff" table (optional, just for example)
# def drop_table_staff():
#     with engine.connect() as conn:
#         conn.execute('DROP TABLE IF EXISTS staff')

# Run all migrations
def run_migrations():
    print("Running migrations...")
    # add_email_to_students()
    # Add any new migrations here

if __name__ == '__main__':
    run_migrations()

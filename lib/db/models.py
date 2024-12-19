from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# SQLAlchemy Base
Base = declarative_base()

# Student Model
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    course = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

# Staff Model
class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

# Attendance Model
class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # Can reference both Student and Staff IDs
    user_type = Column(String, nullable=False)  # Either 'student' or 'staff'
    clock_in_time = Column(DateTime)
    clock_out_time = Column(DateTime)
    date = Column(DateTime, default=datetime.now)

# Create Database Engine and Session
engine = create_engine('sqlite:///db/attendance.db')
Base.metadata.create_all(engine)  # Create tables if they don't exist
Session = sessionmaker(bind=engine)

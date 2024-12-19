
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# SQLAlchemy Base
Base = declarative_base()

# Course Model
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    students = relationship("Student", back_populates="course")

# Student Model
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    created_at = Column(DateTime, default=datetime.now)

    course = relationship("Course", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")

# Staff Model
class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    attendances = relationship("Attendance", back_populates="staff")

# Visitor Model
class Visitor(Base):
    __tablename__ = 'visitors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    attendances = relationship("Attendance", back_populates="visitor")

# Attendance Model
class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    clock_in_time = Column(DateTime)
    clock_out_time = Column(DateTime)
    date = Column(Date, default=datetime.now().date)

    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=True)
    visitor_id = Column(Integer, ForeignKey('visitors.id'), nullable=True)

    student = relationship("Student", back_populates="attendances")
    staff = relationship("Staff", back_populates="attendances")
    visitor = relationship("Visitor", back_populates="attendances")

# Create Database Engine and Session
engine = create_engine('sqlite:///db/attendance.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

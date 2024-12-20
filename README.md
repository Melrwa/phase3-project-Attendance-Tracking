# **Attendance Tracking System**

## **Table of Contents**

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Technologies Used](#technologies-used)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Data Models](#database-models)
7. [File Structure](#file-structure)  
8. [Reports](#reports)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## **Project Overview**

The **Attendance Tracking System** is a Command Line Interface (CLI) application that tracks attendance for **students**, **staff**, and **visitors**. It allows users to clock in and clock out, and it records timestamps to generate daily and weekly attendance reports. The system also tracks student courses, staff roles, and visitor reasons for visits.

The system supports a relational database with multiple linked tables using **SQLAlchemy**. It generates Markdown-based attendance reports that can be used for administrative purposes.

---

## **Features**

- **Clock In / Clock Out** for students, staff, and visitors.  
- **CRUD operations** for Students, Staff, Courses, and Visitors.  
- **Track Attendance** with timestamps for clock-in and clock-out.  
- **Report Generation** for daily and weekly reports in **Markdown (.md)** format.  
- **Organized Reports**:

  - Daily Reports: Courses, staff, student clock-ins, and visitor records.  
  - Weekly Reports: Number of clock-ins for students, staff, and visitors.  

---

## **Technologies Used**

- **Programming Language**: Python 3.8+  
- **Database**: SQLAlchemy (Relational Database)  
- **CLI Tool**: Click (for terminal interactivity)  
- **File Generation**: Markdown (.md) reports for easy readability.  

---

## **Installation**

### **1. Clone the repository**

```bash
git clone https://github.com/Melrwa/phase3-project-Attendance-Tracking.git
cd phase3-project-Attendance-Tracking
```

### **2. Create a virtual environment**

```bash

pipenv install
pipenv shell
```

### **3. Set up the database***

Run the following commands to create and initialize the database:

```bash

python3 -m lib.db.models
```

## **Usage**

Run the application using the following command:

```bash

python3 -m lib.cli
```

Once the program starts, you will be presented with a menu like this:

Attendance Tracking System

- ***1. Clock In***
- ***2. Clock Out***
- ***3. Create Student***
- ***4. Create Staff***
- ***5. Create Visitor***
- ***6. Create Course***
- ***7. Generate Daily Report***
- ***8. Generate Weekly Report***
- ***9. Delete Student***
-***10. Delete Staff***
-***11. Delete Visitor***
- ***0. Exit***

### Menu Options

- **1. Clock In: Clock in for a student, staff, or visitor by entering their ID and role.**
- **2. Clock Out: Clock out for a student, staff, or visitor by entering their ID and role.**
- **3. Create Student: Add a new student to the system and assign them a course.**
- **4. Create Staff: Add a new staff member to the system and define their role.**
- **5. Create Visitor: Log a visitor into the system with their name and reason for visit.**
- **6. Create Course: Create a new course that students can enroll in.**
- **7. Generate Daily Report: Generate a report of all attendance activity for the current day.**
- **8. Generate Weekly Report: Generate a summary of attendance activity for the entire week.**
- **9. Delete student: Deletes student from the database.**
- **10. Delete staff: Deletes staff from the database.**
- **11. Delete visitor: Deletes vistor from the database.**
- **0. Exit: Exit the application.**

---

## **Database Models**

- **Student**: Represents students with a `name` and assigned `course_id`.
- **Staff**: Represents staff members with a `name` and `role`.
- **Visitor**: Represents visitors with a `name`, `reason`, and visit information.
- **Course**: Represents courses that students can clock into.
- **Attendance**: Tracks clock-in and clock-out times for students, staff, and visitors.

## **File Structure**

```bash

├── db
│   ├── attendance.db #Database where information is stored
│   └── __init__.py 
├── lib
│   ├── cli.py      # The main CLI logic for handling menu options
│   ├── db
│   │   ├── migrate.py #Helps with table migration when necessary 
│   │   └── models.py   # Database models for Students, Staff, Visitors, Courses, and Attendance, Defines relationship
│   ├── helpers.py  # Helper functions (optional)
│   ├── __init__.py #Heped run program from  root directory
│   ├── __main__.py 
│   └── reports.py     # Logic to generate daily and weekly Markdown reports
├── Pipfile  # Pipenv configuration file
├── Pipfile.lock # Pipenv lock file
├── README.md  # Project documentation (this file)
└── reports # Directory where daily and weekly reports are saved
    ├── daily_report.md 
    └── weekly_report.md
```

## **Reports**

The system generates daily and weekly reports in the reports/ directory.

## ***Daily Report***

The daily report provides a detailed summary of attendance for the current day (starting at 6:00 am). The report includes:

- **Courses Clocked Into**: Students grouped by course, showing their clock-in and clock-out times.
- **Staff Clocked In**: Staff members who clocked in, along with their clock-in and clock-out times.
- **Visitors**: List of visitors, their reason for visiting, and their clock-in and clock-out times.
- **All Students and Their Courses**: List of all students and the courses they are enrolled in.
- **All Staff and Their Roles**: List of all staff members and their roles.

## ***Weekly Report***

The weekly report tracks attendance over the past 7 days, starting from Monday. It includes:

- **Students Clocked In**: Number of clock-ins per student during the week.
- **Staff Clocked In**: Number of clock-ins per staff member during the week.
- **Visitors**: Number of visits per visitor during the week.

The reports are saved in Markdown (.md) format in the reports/ directory. You can view them using any text editor or Markdown viewer.

## **Contributing**

Contributions are much  welcomed!

## **License**

This project is licensed under the [MIT License](https://github.com/Melrwa/phase3-project-Attendance-Tracking/tree/main#) which allows modification, distribution, and use for both personal and commercial purposes.

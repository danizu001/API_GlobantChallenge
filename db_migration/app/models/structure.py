# Import the necessary SQLAlchemy tools to define table columns
from sqlalchemy import Column, Integer, String, DateTime

# Import the base defined in base.py, which allows us to create database models
from .base import Base

# Define the "departments" table
class Department(Base):
    """
    Model for the 'departments' table.

    Columns:
    - id: Unique identifier for each department.
    - department: Name of the department (up to 100 characters).
    """
    __tablename__ = "departments"  # Table name in the database
    id = Column(Integer, primary_key=True)  # ID column (primary key)
    department = Column(String(100))  # Department name (max. 100 characters)

# Define the "jobs" table
class Job(Base):
    """
    Model for the 'jobs' table.

    Columns:
    - id: Unique identifier for the job.
    - job: Job title (up to 100 characters).
    """
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)  # ID column (primary key)
    job = Column(String(100))  # Job title (max. 100 characters)

# Define the "employees" table
class Employee(Base):
    """
    Model for the 'employees' table.

    Columns:
    - id: Unique identifier for the employee.
    - name: Employee's name (up to 100 characters).
    - datetime: Date and time associated with the employee (e.g., hiring or registration).
    - department_id: Identifier of the department to which the employee belongs.
    - job_id: Identifier of the job the employee holds.
    """
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)  # Unique ID for the employee
    name = Column(String(100))  # Employee's name (max. 100 characters)
    datetime = Column(DateTime)  # Date and time related to the employee (e.g., hiring)
    department_id = Column(Integer)  # Relationship with the "departments" table
    job_id = Column(Integer)  # Relationship with the "jobs" table
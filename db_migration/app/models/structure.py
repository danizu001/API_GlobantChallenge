from sqlalchemy import Column, Integer, String, DateTime
from .base import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    department = Column(String(100))

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    job = Column(String(100))

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    datetime = Column(DateTime)
    department_id = Column(Integer)
    job_id = Column(Integer)
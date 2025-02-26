# Import the necessary SQLAlchemy tools to manage the database
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

# Import the base and table models
from .base import Base  # Import the database base
from .structure import Department, Job, Employee, InvalidEmployee  # Import data models

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create the database engine using the connection URL
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """
    Creates the database tables if they do not exist.
    """
    Base.metadata.create_all(bind=engine)

def get_session():
    """
    Generates a database session and automatically closes it when no longer in use.
    
    Usage:
    - Can be used in FastAPI dependencies to handle database sessions.
    """
    db = SessionLocal()  # Creates a new session
    try:
        yield db  # Provides the session for use in an operation
    finally:
        db.close()  # Closes the session when done

def reset_table(table_name: str):
    """
    Deletes all records from a specific table.

    Parameters:
    - table_name (str): The name of the table to reset. Must be "departments", "jobs", or "employees".
    
    Usage:
    - This removes all data from the table without deleting its structure.
    """
    
    # Mapping of table names to their models
    table_map = {
        "departments": Department,
        "jobs": Job,
        "employees": Employee,
        "invalid_employees": InvalidEmployee
    }
    
    db = SessionLocal()  # Start a database session
    try:
        # Prepare the statement to delete all data from the selected table
        stmt = delete(table_map[table_name])
        db.execute(stmt)  # Execute the statement in the database
        db.commit()  # Save the changes
    except Exception as e:
        db.rollback()  # Roll back the changes if an error occurs
        raise e  # Re-raise the error
    finally:
        db.close()  # Close the database session
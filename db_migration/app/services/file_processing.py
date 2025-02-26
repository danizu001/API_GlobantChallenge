# Import pandas and numpy for data manipulation and cleaning
import pandas as pd
import numpy as np

# Import the insert function to perform database insertions with SQLAlchemy
from sqlalchemy import insert

# Import the exception class to handle SQLAlchemy errors
from sqlalchemy.exc import SQLAlchemyError

# Import the database session from our configuration
from app.models.database import SessionLocal

# Import the database table models
from app.models.structure import Department, Job, Employee

# Dictionary defining the expected column names for each table
TABLE_COLUMNS = {
    "departments": ["id", "department"],  # Departments table
    "jobs": ["id", "job"],  # Jobs table
    "employees": ["id", "name", "datetime", "department_id", "job_id"]  # Employees table
}


async def process_csv(table_name: str, chunk):
    """
    Processes a CSV file and inserts it into the database.

    Params:
    - table_name (str): Name of the table where the data will be inserted. Must be "departments", "jobs", or "employees".
    - chunk (DataFrame): A fragment of the CSV file represented as a pandas DataFrame.

    Raises:
    - ValueError: If the table name is invalid or the number of columns does not match the expected structure.
    - RuntimeError: If an error occurs during database insertion.
    """
    # Create a database session
    session = SessionLocal()
    try:
        # Validate that the table name is valid
        if table_name not in TABLE_COLUMNS:
            raise ValueError(f"Invalid table: {table_name}")

        # Get the expected column names for the table
        column_names = TABLE_COLUMNS[table_name]
        
        # Validate that the number of columns in the CSV matches the table
        if chunk.shape[1] != len(column_names):
            raise ValueError(
                f"Incorrect number of columns. Expected: {len(column_names)}, Received: {chunk.shape[1]}"
            )
        
        # Assign column names to the DataFrame
        chunk.columns = column_names

        # If processing the employees table, perform specific cleaning
        if table_name == "employees":
            # Define columns that should be numeric
            numeric_cols = ["id", "department_id", "job_id"]

            # Convert these columns to numeric values, coercing errors to NaN
            chunk[numeric_cols] = chunk[numeric_cols].apply(pd.to_numeric, errors="coerce")

            # Drop rows where there are NaN values in these columns (Potential change in the next commit to accept null values)
            chunk = chunk.dropna(subset=numeric_cols)

            # Convert columns to integers using Int64 to handle null values
            chunk[numeric_cols] = chunk[numeric_cols].astype("Int64")
            
            # Convert the date column to datetime, ignoring errors
            chunk["datetime"] = pd.to_datetime(chunk["datetime"], errors="coerce")

            # Drop rows with NaN values in the date column (Potential change in the next commit to accept null values)
            chunk = chunk.dropna(subset=["datetime"])

        # Convert the DataFrame into a list of dictionaries for database insertion
        data = chunk.to_dict(orient="records")
        
        # Map the table name to its SQLAlchemy model
        table_map = {
            "departments": Department,
            "jobs": Job,
            "employees": Employee
        }

        # Prepare the SQL statement to insert data into the corresponding table
        stmt = insert(table_map[table_name]).values(data)

        # Execute the database insertion
        session.execute(stmt)

        # Commit the changes to the database
        session.commit()

    except SQLAlchemyError as e:
        # If there is a database error, roll back the transaction
        session.rollback()
        raise RuntimeError(f"Database error: {str(e)}") from e
    except Exception as e:
        # Capture other unexpected errors
        raise RuntimeError(f"Unexpected error: {str(e)}") from e
    finally:
        # Close the database session
        session.close()

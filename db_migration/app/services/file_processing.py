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
from app.models.structure import Department, Job, Employee, InvalidEmployee  # Nueva tabla para registros inválidos

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

            # Convert the date column to datetime, ignoring errors
            chunk["datetime"] = pd.to_datetime(chunk["datetime"], errors="coerce")

            # Separar registros válidos e inválidos
            # Un registro es inválido si tiene valores nulos en department_id, job_id o datetime
            invalid_mask = (
                chunk["department_id"].isna() |
                chunk["job_id"].isna() |
                chunk["datetime"].isna()
            )
            valid_data = chunk[~invalid_mask]  # Registros válidos
            invalid_data = chunk[invalid_mask]  # Registros inválidos

            # Insertar registros válidos en la tabla employees
            if not valid_data.empty:
                valid_records = valid_data.to_dict(orient="records")
                stmt = insert(Employee).values(valid_records)
                session.execute(stmt)

            # Insertar registros inválidos en la tabla invalid_employees
            if not invalid_data.empty:
                invalid_records = invalid_data.to_dict(orient="records")
                for record in invalid_records:
                    # Convertir NaN a None para que SQLAlchemy lo maneje como NULL
                    for key in record:
                        if pd.isna(record[key]):
                            record[key] = None
                    # Agregar un campo adicional para almacenar la razón del error
                    record["error_reason"] = "Invalid foreign key or datetime"
                stmt = insert(InvalidEmployee).values(invalid_records)
                session.execute(stmt)

            # Commit los cambios a la base de datos
            session.commit()

        else:
            # Para las tablas departments y jobs, insertar todos los registros directamente
            data = chunk.to_dict(orient="records")
            table_map = {
                "departments": Department,
                "jobs": Job
            }
            stmt = insert(table_map[table_name]).values(data)
            session.execute(stmt)
            session.commit()

    except SQLAlchemyError as e:
        # Si hay un error en la base de datos, hacer rollback de la transacción
        session.rollback()
        raise RuntimeError(f"Database error: {str(e)}") from e
    except Exception as e:
        # Capturar otros errores inesperados
        raise RuntimeError(f"Unexpected error: {str(e)}") from e
    finally:
        # Cerrar la sesión de la base de datos
        session.close()
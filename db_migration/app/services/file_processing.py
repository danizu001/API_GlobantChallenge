import pandas as pd
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import SessionLocal
from app.models.structure import Department, Job, Employee

TABLE_COLUMNS = {
    "departments": ["id", "department"],
    "jobs": ["id", "job"],
    "employees": ["id", "name", "datetime", "department_id", "job_id"]
}

async def process_csv(table_name: str, chunk):
    session = SessionLocal()
    try:
        if table_name not in TABLE_COLUMNS:
            raise ValueError(f"Invalid table: {table_name}")

        column_names = TABLE_COLUMNS[table_name]
        if chunk.shape[1] != len(column_names):
            raise ValueError(
                f"Incorrect number of columns. Expected: {len(column_names)}, Received: {chunk.shape[1]}"
            )

        chunk.columns = column_names

        if table_name == "employees":
            numeric_cols = ["id", "department_id", "job_id"]
            chunk[numeric_cols] = chunk[numeric_cols].apply(pd.to_numeric, errors="coerce")
            chunk = chunk.dropna(subset=numeric_cols)
            chunk[numeric_cols] = chunk[numeric_cols].astype("Int64")
            chunk["datetime"] = pd.to_datetime(chunk["datetime"], errors="coerce")
            chunk = chunk.dropna(subset=["datetime"])

        data = chunk.to_dict(orient="records")

        table_map = {
            "departments": Department,
            "jobs": Job,
            "employees": Employee
        }
        stmt = insert(table_map[table_name]).values(data)
        session.execute(stmt)
        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"Database error: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}") from e
    finally:
        session.close()

def process_csv_from_path(table_name: str, file_path: str):
    try:
        chunks = pd.read_csv(file_path, header=None, sep=",", chunksize=1000)
        for chunk in chunks:
            process_csv(table_name, chunk)
    except Exception as e:
        raise RuntimeError(f"Error processing CSV file: {str(e)}")
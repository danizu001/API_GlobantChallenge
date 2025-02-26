from sqlalchemy import create_engine, delete, inspect
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from .base import Base
from .structure import Department, Job, Employee

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_table(table_name: str):
    table_map = {
        "departments": Department,
        "jobs": Job,
        "employees": Employee
    }
    
    db = SessionLocal()
    try:
        stmt = delete(table_map[table_name])
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
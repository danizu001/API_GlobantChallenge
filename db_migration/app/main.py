from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.models.database import create_db_and_tables, reset_table
from app.services.file_processing import process_csv_from_path

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="DB Migration API", lifespan=lifespan)

# Ruta temporal para probar el reseteo de tablas
@app.post("/test-reset/{table_name}")
async def test_reset(table_name: str):
    reset_table(table_name)
    return {"message": f"Table '{table_name}' reset successfully"}

# Ruta temporal para cargar un CSV desde una ruta
@app.post("/test-load-csv/{table_name}")
async def test_load_csv(table_name: str, file_path: str):
    try:
        process_csv_from_path(table_name, file_path)
        return {"message": f"CSV file '{file_path}' processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
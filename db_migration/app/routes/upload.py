from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services.file_processing import process_csv
import pandas as pd
from app.models.database import reset_table


router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/csv/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = File(...)):
    try:
        # Validar tabla permitida
        if table_name not in ["departments", "jobs", "employees"]:
            raise HTTPException(status_code=400, detail="Tabla no válida")

        # Procesar CSV en lotes
        df = pd.read_csv(file.file, header=None, sep=",", chunksize=1000)
        for chunk in df:
            await process_csv(table_name, chunk)

        return JSONResponse(content={"message": "Datos cargados exitosamente"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reset/{table_name}")
async def reset_table_endpoint(table_name: str):
    try:
        reset_table(table_name)
        return {"message": f"Tabla {table_name} reseteada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Import APIRouter to define routes in FastAPI.
# Also, import UploadFile and File to handle file uploads.
# HTTPException is used to manage errors, and JSONResponse to send responses in JSON format.
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# Import the process_csv function, which will handle CSV file processing.
from ..services.file_processing import process_csv
import pandas as pd

# Import reset_table to clear a database table if necessary.
from app.models.database import reset_table

# Create a router to group all routes related to file uploads.
router = APIRouter(prefix="/upload", tags=["Upload"])

# Route to upload a CSV file to a specific table
@router.post("/csv/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = File(...)):
    """
    Uploads a CSV file and processes it in the database.

    Params:
    - table_name (str): Name of the table where the data will be inserted. Must be "departments", "jobs", or "employees".
    - file (UploadFile): CSV file to be uploaded.

    Returns:
    - JSONResponse: Success or error message.
    """
    try:
        # Verify that the table is valid
        if table_name not in ["departments", "jobs", "employees"]:
            raise HTTPException(status_code=400, detail="Invalid table")

        # Read the CSV file in chunks of 1000 rows as specified
        df = pd.read_csv(file.file, header=None, sep=",", chunksize=1000)
        
        # Process each chunk of the CSV file
        for chunk in df:
            await process_csv(table_name, chunk)

        # If everything goes well, send a success response
        return JSONResponse(content={"message": "Data uploaded successfully"})
    
    except Exception as e:
        # If an error occurs, send an error message with status code 500
        raise HTTPException(status_code=500, detail=str(e))

# Route to reset a database table
@router.delete("/reset/{table_name}")
async def reset_table_endpoint(table_name: str):
    """
    Resets a database table.

    Params:
    - table_name (str): Name of the table to be reset.

    Returns:
    - dict: Success or error message.
    """
    try:
        # Call the function that resets the table
        reset_table(table_name)
        
        # Send a success message
        return {"message": f"Table {table_name} reset successfully"}
    
    except Exception as e:
        # In case of an error, send an error message with status code 500
        raise HTTPException(status_code=500, detail=str(e))

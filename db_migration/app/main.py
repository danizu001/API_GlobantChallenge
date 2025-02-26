# Import FastAPI to create the web application
from fastapi import FastAPI

# Import asynccontextmanager to manage the application lifecycle
from contextlib import asynccontextmanager

# Import the function to create the database and tables
from app.models.database import create_db_and_tables

# Import the router that handles file upload routes
from app.routes.upload import router as upload_router

# Define an application lifecycle handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database and tables when the application starts
    create_db_and_tables()
    yield  # Continue with application execution

# Create the FastAPI instance with the defined lifecycle
app = FastAPI(title="DB Migration API", lifespan=lifespan)

# Include file upload-related routes in the application
app.include_router(upload_router)

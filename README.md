# DB Migration API

REST API for migrating historical data from CSV files to an SQL database.


## Key Features
- **Bulk CSV Upload**: Inserts up to 1000 records per transaction  
- **Multiple Tables**: Supports `departments`, `jobs`, and `employees`  
- **Data Validation**: Handles formats and duplicates  
- **Safe Reset**: Endpoint to clear specific tables  
- **Interactive Documentation**: Integrated with Swagger UI  

## Quick Installation

```bash
# Clone repository
git clone https://github.com/tu_usuario/db_migration.git
cd db_migration

# Set up virtual environment (Python 3.11+)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

## Upload Files

```bash
# Departments
curl -X POST -F "file=@data/CSV_files/departments.csv" http://localhost:8000/upload/csv/departments

# Jobs
curl -X POST -F "file=@data/CSV_files/jobs.csv" http://localhost:8000/upload/csv/jobs

# Employees
curl -X POST -F "file=@data/CSV_files/hired_employees.csv" http://localhost:8000/upload/csv/employees

# Reset any table example:
curl -X DELETE http://localhost:8000/upload/reset/employees
```

## Structure
```
db_migration/
├── app/
│   ├── models/
│   │   ├── __init__.py  # Initializes the models module
│   │   ├── base.py  # Defines the base class for SQLAlchemy models
│   │   ├── database.py  # Sets up database connection and sessions
│   │   └── structure.py  # Defines table models (departments, jobs, employees)
│   ├── routes/
│   │   ├── __init__.py  # Initializes the routes module
│   │   └── upload.py  # Defines API endpoints for uploading and handling CSV files
│   ├── services/
│   │   ├── __init__.py  # Initializes the services module
│   │   └── file_processing.py  # Contains logic for processing and validating CSV files
│   ├── __init__.py  # Initializes the main application module
│   └── main.py  # Application entry point, sets up FastAPI and routers
├── data/
│   ├── CSV_files/
│   │   ├── departments.csv  # CSV file with department data
│   │   ├── hired_employees.csv  # CSV file with employee data
│   │   └── jobs.csv  # CSV file with job data
│   └── migration.db  # SQLite database file
├── tests/
├── .env # Environment variables file (included in GitHub as it does not contain sensitive information!!!!!)
├── config.py # Project configuration, including file paths
├── requirements.txt # Project dependencies
.gitignore # Ignore files such as pycache
README # Project instructions
```
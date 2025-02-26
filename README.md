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

There are some info in the employees.csv that have null data so is going to create that rows in a separate table due to the integrity of the data.

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

## Get option
These commands are going to save in your current directory the result in a json file.
**(Is going to take the values of both tables employees and invalid_employees not only employees!!!!!).**

```bash
#End-point 1 
curl -X GET "http://localhost:8000/metrics/hires-by-quarter" -o hires_by_quarter.json

#End-point 2
curl -X GET "http://localhost:8000/metrics/departments-above-mean" -o departments_above_mean.json

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
│   │   ├── get.py  # Define API endpoints to get the asked info
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
├── departments_above_mean.json #Result of the endpoint
├── hires_by_quarter.json #Result of the end point
├── Dockerfile #Dockerfile
.gitignore # Ignore files such as pycache
README # Project instructions
```

## Dockerfile
To execute the API in a docker container please go ahead with the next steps:
```bash
#Create the image
docker build -t my-fastapi-app .
#Create the container
docker run -d -p 8000:8000 my-fastapi-app
```
Keep in mind that the container has already the DB filled with the csv files, if you want to test run these commands.
```bash
curl -X DELETE http://localhost:8000/upload/reset/invalid_employees  
curl -X DELETE http://localhost:8000/upload/reset/employees  
curl -X DELETE http://localhost:8000/upload/reset/jobs  
curl -X DELETE http://localhost:8000/upload/reset/departments 
curl -X POST -F "file=@data/CSV_files/departments.csv" http://localhost:8000/upload/csv/departments
curl -X POST -F "file=@data/CSV_files/jobs.csv" http://localhost:8000/upload/csv/jobs
curl -X POST -F "file=@data/CSV_files/hired_employees.csv" http://localhost:8000/upload/csv/employees
```

## Docker-Compose
To execute the API with PostgreSQL in docker-compose run the next commands:
```bash
#Create the image
docker-compose build
#Create the container
docker-compose up
```
**Benefits instead docker image**
- **PostgreSQL**: We are using PostgreSQL instead of SQLite 
- **Volume**: We have data persistance it mean if we stop the container and start it again. The DB will keep the same info  
- **Scale**: We have the possibility to scale services

## Amazon
The last update of the project is the deployment of the image in ECS and ECR

- **AWS ECS (Fargate)**: Execute containers serverless.
Use the next commands to update de DB
```bash
curl -X POST -F "file=@data/CSV_files/departments.csv" http://44.200.73.84:8000/upload/csv/departments
curl -X POST -F "file=@data/CSV_files/jobs.csv" http://44.200.73.84:8000/upload/csv/jobs
curl -X POST -F "file=@data/CSV_files/demployees.csv" http://44.200.73.84:8000/upload/csv/employees
curl -X DELETE http://44.200.73.84:8000/upload/reset/invalid_employees  
curl -X DELETE http://44.200.73.84:8000/upload/reset/employees  
curl -X DELETE http://44.200.73.84:8000/upload/reset/jobs  
curl -X DELETE http://44.200.73.84:8000/upload/reset/departments 
```
If some of those commands doesn't work try to do the opposite you are doing eg. instead of post try to delete de database maybe there is information in the DB.


## Test
Future updates in the repository
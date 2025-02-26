from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.models.database import SessionLocal

# Create a router to group the query endpoints
router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/hires-by-quarter")
async def hires_by_quarter():
    """
    Endpoint to get the number of employees hired per job and department in 2021, divided by quarter.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains:
            - department (str): Name of the department.
            - job (str): Name of the job.
            - Q1 (int): Number of employees hired in the first quarter.
            - Q2 (int): Number of employees hired in the second quarter.
            - Q3 (int): Number of employees hired in the third quarter.
            - Q4 (int): Number of employees hired in the fourth quarter.

    Raises:
        HTTPException: If an error occurs during the query execution.
    """
    try:
        # SQL query to get the data
        query = text("""
            SELECT 
                d.department AS department,
                j.job AS job,
                SUM(CASE WHEN strftime('%m', e.datetime) IN ('01', '02', '03') THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN strftime('%m', e.datetime) IN ('04', '05', '06') THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN strftime('%m', e.datetime) IN ('07', '08', '09') THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN strftime('%m', e.datetime) IN ('10', '11', '12') THEN 1 ELSE 0 END) AS Q4
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            JOIN jobs j ON e.job_id = j.id
            WHERE strftime('%Y', e.datetime) = '2021'
            GROUP BY d.department, j.job
            ORDER BY d.department, j.job;
        """)
        
        # Execute the query
        with SessionLocal() as session:
            result = session.execute(query)
            rows = result.fetchall()
        
        # Format the response
        response = [{
            "department": row[0],
            "job": row[1],
            "Q1": row[2],
            "Q2": row[3],
            "Q3": row[4],
            "Q4": row[5]
        } for row in rows]
        
        return response

    except Exception as e:
        # Catch errors and return an HTTP 500 response
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/departments-above-mean")
async def departments_above_mean():
    """
    Endpoint to get the list of departments that hired more employees than the mean in 2021.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains:
            - id (int): ID of the department.
            - department (str): Name of the department.
            - hired (int): Number of employees hired in 2021.

    Raises:
        HTTPException: If an error occurs during the query execution.
    """
    try:
        # SQL query to get the data
        query = text("""
            WITH department_hires AS (
                SELECT 
                    d.id AS id,
                    d.department AS department,
                    COUNT(e.id) AS hired
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                WHERE strftime('%Y', e.datetime) = '2021'
                GROUP BY d.id, d.department
            ),
            mean_hires AS (
                SELECT AVG(hired) AS mean_hired
                FROM department_hires
            )
            SELECT 
                dh.id,
                dh.department,
                dh.hired
            FROM department_hires dh
            CROSS JOIN mean_hires mh
            WHERE dh.hired > mh.mean_hired
            ORDER BY dh.hired DESC;
        """)
        
        # Execute the query
        with SessionLocal() as session:
            result = session.execute(query)
            rows = result.fetchall()
        
        # Format the response
        response = [{
            "id": row[0],
            "department": row[1],
            "hired": row[2]
        } for row in rows]
        
        return response

    except Exception as e:
        # Catch errors and return an HTTP 500 response
        raise HTTPException(status_code=500, detail=str(e))
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import employee as employee_schema
from app.utils import excel_parser

router = APIRouter()


@router.post("/upload/", response_model=List[employee_schema.Employee])
async def create_employees_from_excel(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Upload an Excel file to create new employees.
    """
    try:
        employees = excel_parser.parse_excel_file(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_employees = excel_parser.save_employees_to_db(db, employees)
    return [
        employee_schema.Employee(
            id=db_employee.id,
            first_name=db_employee.first_name,
            last_name=db_employee.last_name,
            phone_number=db_employee.phone_number,
            company_id=db_employee.company_id,
            company_name=db_employee.company.name,  # Access company name from the relationship
        )
        for db_employee in db_employees
    ]

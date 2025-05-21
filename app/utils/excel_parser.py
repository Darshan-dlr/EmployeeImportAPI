import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.employee import Company, Employee
from app.schemas import employee as employee_schema


def parse_excel_file(file):
    """Parses the excel file and returns a list of EmployeeCreate objects."""
    try:
        df = pd.read_excel(file)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {str(e)}")

    employees = []
    for _, row in df.iterrows():
        try:
            employee = employee_schema.EmployeeCreate(
                first_name=row["FIRST_NAME"],
                last_name=row["LAST_NAME"],
                phone_number=row["PHONE_NUMBER"],
                company_name=row["COMPANY_NAME"],
            )
            employees.append(employee)
        except KeyError as e:
            raise ValueError(f"Missing column in Excel file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing row: {str(e)}")
    return employees


def save_employees_to_db(db: Session, employee_creates: List[employee_schema.EmployeeCreate]):
    """Saves the employees to the database."""
    companies = {}
    employees = []

    for employee_create in employee_creates:
        company_name = employee_create.company_name
        if company_name not in companies:
            company = db.query(Company).filter(Company.name == company_name).first()
            if not company:
                company = Company(name=company_name)
                db.add(company)
                db.flush()  # Get the ID immediately after adding
            companies[company_name] = company.id

        employee = Employee(
            first_name=employee_create.first_name,
            last_name=employee_create.last_name,
            phone_number=employee_create.phone_number,
            company_id=companies[company_name],
        )
        employees.append(employee)

    db.add_all(employees)
    db.commit()

    return employees
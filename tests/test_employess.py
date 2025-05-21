import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from app.core.database import Base, get_db
from main import app
from app.models.employee import Company, Employee
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_test_excel(filename="test.xlsx"):
    """Creates a sample test Excel file."""
    data = {
        "FIRST_NAME": ["John", "Alice"],
        "LAST_NAME": ["Doe", "Smith"],
        "PHONE_NUMBER": ["123-456-7890", "987-654-3210"],
        "COMPANY_NAME": ["Acme Corp", "Beta Inc"],
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


def test_create_employee(test_db):
    create_test_excel()  
    response = client.post(
        "/employees/upload/",
        files={
            "file": (
                "test.xlsx",
                open("test.xlsx", "rb"),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 2  # Verify that two employees were created

    # Verify the data in the database
    db = TestingSessionLocal()
    try:
        employees = db.query(Employee).all()
        assert len(employees) == 2
        assert employees[0].first_name == "John"
        assert employees[1].last_name == "Smith"
    finally:
        db.close()


def test_create_employee_invalid_file(test_db):
    response = client.post(
        "/employees/upload/", files={"file": ("invalid.txt", b"some random content")}
    )
    assert response.status_code == 400  # Expect a 400 error for invalid file


def test_create_employee_missing_column(test_db):
    data = {"FIRST_NAME": ["John"], "LAST_NAME": ["Doe"]}
    df = pd.DataFrame(data)
    df.to_excel("test.xlsx", index=False)

    response = client.post(
        "/employees/upload/",
        files={
            "file": (
                "test.xlsx",
                open("test.xlsx", "rb"),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 400  # Expect a 400 error for missing columns
    
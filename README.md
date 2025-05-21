
# Employee Import API

## Description

This API allows you to import employee data from Excel files into a database. It uses FastAPI, SQLAlchemy, and MySQL.

## File Structure

```
EmployeeImportAPI/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── employees.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── employee.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── employee.py
│   └── utils/
│       ├── __init__.py
│       └── excel_parser.py
├── tests/
│   ├── __init__.py
│   └── test_employees.py
├── README.md
├── .gitignore
├── requirements.txt
├── main.py
└── .env
└── Practical Task Python sheet .xlsx
```

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd EmployeeImportAPI
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Linux/macOS
    venv\Scripts\activate.bat  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database:**

    *   Create a `.env` file in the root directory and add your database URL:

        ```
        DATABASE_URL="mysql+mysqlconnector://user:password@host/database"
        ```

    *   The application reads the `DATABASE_URL` from the `.env` file using the `python-dotenv` library.  Ensure that the `.env` file is in the root directory and that the `DATABASE_URL` is correctly configured.

5.  **Run the application:**

    ```bash
    uvicorn main:app --reload
    ```

## API Endpoints

### `POST /employees/upload/`

Upload an Excel file to create new employees.

*   **Request Body:**  `file` (Excel file)
*   **Response:**  A list of created employees.

## Swagger Documentation

You can access the Swagger documentation at `/docs` or `/redoc` after running the application.

## Running Tests

1.  Ensure you have a `test.xlsx` file in the root directory for testing the upload functionality. You can use the `create_test_excel` function in `tests/test_employees.py` to generate a sample file.
2.  To run the tests, use the following command:

    ```bash
    pytest
    ```

    The tests will automatically use the database URL configured in your `.env` file.
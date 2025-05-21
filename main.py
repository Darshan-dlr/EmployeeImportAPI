from fastapi import FastAPI
from app.api.endpoints import employees
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Employee Import API",
    description="API to import employee data from Excel files into a database.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",  # Add your frontend URL here
    "*",  # REMOVE IN PRODUCTION - Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(employees.router, prefix="/employees", tags=["employees"])


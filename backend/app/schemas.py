from pydantic import BaseModel, Field, validator
from datetime import date, time
from typing import Literal

# Movie Schema
class MovieBase(BaseModel):
    title: str
    genre: Literal[
        "Comedy", "Romance", "Action", "Horror", "Sci-Fi", 
        "Fantasy", "Thriller", "Drama", "Mystery", "Documentary"
    ]
    age_limit: bool
    director: str
    duration_minutes: int
    release_date: date
    critics_rating: float

    @validator("release_date")
    def validate_release_date(cls, value):
        if value < date(1970, 1, 1):
            raise ValueError("Release date must be on or after January 1, 1970.")
        return value

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True


# Employee Schema
class EmployeeBase(BaseModel):
    personal_id: str
    phone_number: str = Field(..., pattern=r"^\d+$", description="Phone number must contain only digits.")
    first_name: str
    last_name: str
    birth_year: date
    start_year: date
    role: Literal[
        "Cashier", "Canteen Seller", "Warehouse Worker", 
        "Customer Center Worker", "Ticket Seller", "Manager"
    ]
    city: str
    salary: float

    @validator("birth_year", "start_year")
    def validate_years(cls, value):
        if value < date(1970, 1, 1):
            raise ValueError("Date must be on or after January 1, 1970.")
        return value

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


# Branch Schema
class BranchBase(BaseModel):
    name: str
    manager_id: str
    opening_time: time
    closing_time: time
    opening_year: date
    customer_service_phone: str = Field(..., pattern=r"^\d+$", description="Phone number must contain only digits.")

    @validator("opening_year")
    def validate_opening_year(cls, value):
        if value < date(1970, 1, 1):
            raise ValueError("Opening year must be on or after January 1, 1970.")
        return value

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: int

    class Config:
        orm_mode = True


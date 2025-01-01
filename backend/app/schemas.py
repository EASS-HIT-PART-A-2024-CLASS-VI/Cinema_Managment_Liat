from pydantic import BaseModel
from datetime import date, time

class MovieBase(BaseModel):
    title: str
    genre: str
    age_limit: bool
    director: str
    duration_minutes: int
    release_date: date
    critics_rating: float

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    personal_id: str
    phone_number: str
    first_name: str
    last_name: str
    birth_year: date
    start_year: date
    role: str
    city: str
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

class BranchBase(BaseModel):
    name: str
    manager_id: str
    opening_time: time
    closing_time: time
    opening_year: date
    customer_service_phone: str

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: int

    class Config:
        orm_mode = True



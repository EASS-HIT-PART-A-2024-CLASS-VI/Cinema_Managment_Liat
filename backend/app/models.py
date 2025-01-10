from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String, nullable=False)
    age_limit = Column(Boolean, nullable=False)
    director = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    critics_rating = Column(Float, nullable=False)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    personal_id = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_year = Column(Date, nullable=False)
    start_year = Column(Date, nullable=False)
    role = Column(String, nullable=False)
    city = Column(String, nullable=False)
    salary = Column(Float, nullable=False)

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    manager_id = Column(String, nullable=False)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    opening_year = Column(Date, nullable=False)
    customer_service_phone = Column(String, nullable=False)

class Permission(Base):
    __tablename__ = "permissions"
    username = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(String, nullable=False)


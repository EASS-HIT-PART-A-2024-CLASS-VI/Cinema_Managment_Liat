from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manager_id = Column(String, unique=True)
    opening_time = Column(String)
    closing_time = Column(String)
    opening_year = Column(Integer)
    customer_service_phone = Column(String)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    personal_id = Column(String, unique=True)
    phone_number = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birth_year = Column(Integer)
    start_year = Column(Integer)
    role = Column(String)
    city = Column(String)
    salary = Column(Float)
    branch_id = Column(Integer, ForeignKey('branches.id'))
    branch = relationship('Branch', back_populates="employees")

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    age_limit = Column(Boolean)
    director = Column(String)
    duration_minutes = Column(Integer)
    release_date = Column(DateTime)
    critics_rating = Column(Float)

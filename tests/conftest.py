import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from backend.app.main import app, get_db
from backend.app.models import Base
from datetime import datetime
import random
import string

# Helper function for generating unique values
def generate_unique_value(length=9, char_set=None):
    """
    Generate a unique value with optional character set.
    
    Args:
        length (int): Length of the generated string
        char_set (str, optional): Character set to use. Defaults to digits.
    
    Returns:
        str: Unique generated string
    """
    if char_set is None:
        char_set = string.digits
    return ''.join(random.choices(char_set, k=length))

def generate_unique_id():
    """Generate a unique 9-digit ID."""
    return generate_unique_value(9)

def generate_unique_name():
    """Generate a unique 8-character name."""
    return generate_unique_value(8, string.ascii_letters)

def generate_unique_phone():
    """Generate a unique 10-digit phone number."""
    return generate_unique_value(10)

# Database Configuration for Testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_cinema.db"

# Create test database engine with specific configuration for SQLite
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Core Testing Fixtures
@pytest.fixture(scope="function")
def test_db():
    """
    Creates a new database session for testing and rolls back changes after each test.
    
    Yields:
        Session: A SQLAlchemy session for testing
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # Rollback and close the session
        db.rollback()
        db.close()
        
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    """
    Provides a test client with an overridden database dependency.
    
    Args:
        test_db: The test database session
        
    Yields:
        TestClient: A FastAPI TestClient instance
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear the override
    app.dependency_overrides.clear()

# Movie Fixtures
@pytest.fixture
def sample_movie_data():
    """
    Provides sample movie data for testing movie creation and updates.
    
    The data follows the MovieCreate schema with valid genre and rating values.
    """
    return {
        "title": f"Test Movie {generate_unique_name()}",
        "genre": "Action",
        "age_limit": False,
        "director": "Test Director",
        "duration_minutes": 120,
        "release_date": "2024-01-01",
        "critics_rating": 8.5
    }

@pytest.fixture
def sample_movie_sorted_data():
    """
    Provides sample movie data with higher rating for testing sorting functionality.
    """
    return {
        "title": f"High Rated Movie {generate_unique_name()}",
        "genre": "Drama",
        "age_limit": True,
        "director": "Test Director",
        "duration_minutes": 150,
        "release_date": "2024-02-01",
        "critics_rating": 9.5
    }

# Employee Fixtures
@pytest.fixture
def sample_employee_data():
    """
    Provides sample employee data for testing employee creation and updates.
    """
    return {
        "personal_id": generate_unique_id(),
        "phone_number": generate_unique_phone(),
        "first_name": f"Test{generate_unique_name()}",
        "last_name": "Employee",
        "birth_year": "1990-01-01",
        "start_year": "2020-01-01",
        "role": "Cashier",
        "city": "Test City",
        "salary": 30000.0
    }

@pytest.fixture
def sample_manager_data():
    """
    Creates sample manager data that can be used for both employee creation
    and branch management.
    """
    manager_name = generate_unique_name()
    return {
        "personal_id": generate_unique_id(),
        "phone_number": generate_unique_phone(),
        "first_name": f"Manager{manager_name}",
        "last_name": "Test",
        "birth_year": "1985-01-01",
        "start_year": "2015-01-01",
        "role": "Manager",
        "city": "Test City",
        "salary": 50000.0
    }

# Branch Fixtures
@pytest.fixture
def sample_branch_data(sample_manager_data):
    """
    Provides sample branch data for testing branch operations.
    """
    return {
        "name": f"Branch {generate_unique_name()}",
        "manager_id": sample_manager_data["personal_id"],
        "opening_time": "09:00:00",
        "closing_time": "22:00:00",
        "opening_year": "2020-01-01",
        "customer_service_phone": generate_unique_phone()
    }

# Authentication Fixtures
@pytest.fixture
def sample_login_data(sample_manager_data):
    """
    Provides sample login credentials for testing authentication.
    """
    return {
        "username": sample_manager_data["first_name"],
        "password": "Aa123456"
    }

# LLM Service Fixtures
@pytest.fixture
def sample_llm_request():
    """
    Provides sample data for testing the LLM chat integration.
    """
    return {
        "prompt": f"Test prompt {generate_unique_name()}",
        "context": f"Test context {generate_unique_name()}"
    }

# Sorting and Filtering Fixtures
@pytest.fixture
def sample_sorted_employees_data():
    """
    Provides a list of employees with different salaries for testing
    the salary sorting functionality.
    """
    return [
        {
            "personal_id": generate_unique_id(),
            "phone_number": generate_unique_phone(),
            "first_name": "High",
            "last_name": "Salary",
            "birth_year": "1990-01-01",
            "start_year": "2020-01-01",
            "role": "Manager",
            "city": "Test City",
            "salary": 60000.0
        },
        {
            "personal_id": generate_unique_id(),
            "phone_number": generate_unique_phone(),
            "first_name": "Medium",
            "last_name": "Salary",
            "birth_year": "1995-01-01",
            "start_year": "2021-01-01",
            "role": "Cashier",
            "city": "Test City",
            "salary": 40000.0
        }
    ]

@pytest.fixture
def sample_birthday_employee_data():
    """
    Provides sample employee data with birth date in the current month
    for testing the birthday functionality.
    """
    current_month = datetime.now().month
    return {
        "personal_id": generate_unique_id(),
        "phone_number": generate_unique_phone(),
        "first_name": "Birthday",
        "last_name": "Employee",
        "birth_year": f"1992-{current_month:02d}-15",
        "start_year": "2020-01-01",
        "role": "Cashier",
        "city": "Test City",
        "salary": 35000.0
    }
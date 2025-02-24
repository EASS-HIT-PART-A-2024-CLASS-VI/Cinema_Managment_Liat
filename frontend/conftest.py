import os
import sys
import pytest
import streamlit as st 
from unittest.mock import Mock, patch
import requests

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture
def mock_requests():
    """Mock requests to backend API"""
    with patch('requests.get') as mock_get, patch('requests.post') as mock_post, patch('requests.delete') as mock_delete:
        yield {
            'get': mock_get,
            'post': mock_post,
            'delete': mock_delete
        }

@pytest.fixture
def mock_session_state():
    """Mock Streamlit session state"""
    with patch('streamlit.session_state') as mock_state:
        mock_state.authenticated = False
        mock_state.username = None
        mock_state.menu = "Movies"
        mock_state.show_chatbot = False
        mock_state.show_sorted_movies = False
        mock_state.show_sorted_employees = False
        mock_state.show_birthdays = False
        mock_state.manage_screenings = False
        yield mock_state

@pytest.fixture
def sample_movie_data():
    """Sample movie data for testing"""
    test_movie = {
        "id": 1,
        "title": "Test Movie",
        "genre": "Action",
        "age_limit": False,
        "director": "Test Director",
        "duration_minutes": 120,
        "release_date": "2024-01-01",
        "critics_rating": 8.5
    }
    yield test_movie.copy()

@pytest.fixture
def sample_employee_data():
    """Sample employee data for testing"""
    test_employee = {
        "id": 1,
        "personal_id": "123456789",
        "phone_number": "0501234567",
        "first_name": "Test",
        "last_name": "Employee",
        "birth_year": "1990-01-01",
        "start_year": "2020-01-01",
        "role": "Manager",
        "city": "Test City",
        "salary": 30000.0
    }
    yield test_employee.copy()

@pytest.fixture(autouse=True)
def prevent_real_http():
    """Prevent any real HTTP requests during testing"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Real HTTP requests are not allowed during testing!")
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Real HTTP requests are not allowed during testing!")
    with patch('requests.delete') as mock_delete:
        mock_delete.side_effect = Exception("Real HTTP requests are not allowed during testing!")
    yield

@pytest.fixture(autouse=True)
def suppress_streamlit_warnings():
    """Suppress Streamlit missing context warnings"""
    with patch('streamlit.warning') as mock_warning:
        yield mock_warning
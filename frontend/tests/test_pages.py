import pytest
from unittest.mock import patch
import streamlit as st
from pages.movies import movies_page
from pages.employees import employees_page
from pages.branches import branches_page

def test_movies_page(mock_requests, mock_session_state, sample_movie_data):
    """Test movies page functionality"""
    # Mock API responses
    mock_requests['get'].return_value.status_code = 200
    mock_requests['get'].return_value.json.return_value = [sample_movie_data]
    
    with patch('streamlit.header') as mock_header:
        movies_page()
        mock_header.assert_called_once_with("Movies Management")

def test_employees_page(mock_requests, mock_session_state, sample_employee_data):
    """Test employees page functionality"""
    mock_requests['get'].return_value.status_code = 200
    mock_requests['get'].return_value.json.return_value = [sample_employee_data]
    
    with patch('streamlit.header') as mock_header:
        employees_page()
        mock_header.assert_called_once_with("Employees Management")

def test_branches_page(mock_requests, mock_session_state):
    """Test branches page functionality"""
    # Mock the session_state.get method to return False for manage_screenings
    mock_session_state.get.return_value = False
    mock_session_state.authenticated = True

    mock_requests['get'].return_value.status_code = 200
    mock_requests['get'].return_value.json.return_value = [{
        "id": 1,
        "name": "Test Branch",
        "manager_id": "123456789",
        "opening_time": "09:00:00",
        "closing_time": "22:00:00"
    }]

    with patch('streamlit.header') as mock_header, \
         patch('streamlit.radio') as mock_radio:
        
        # Setup mock return for radio button
        mock_radio.return_value = "View Branches"
        
        # Run function
        branches_page()
        
        # Verify header
        mock_header.assert_called_once_with("Branches Management")
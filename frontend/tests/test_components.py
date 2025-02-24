import pytest
from unittest.mock import patch
import streamlit as st

# Use absolute imports
from components.login import login_page
from components.sidebar import sidebar
from components.utils import set_background, get_encoded_background

def test_login_page(mock_requests, mock_session_state):
    """Test login page functionality"""
    # Set initial session state
    mock_session_state.authenticated = False
    
    with patch('streamlit.text_input') as mock_input, \
         patch('streamlit.button') as mock_button, \
         patch('streamlit.markdown') as mock_markdown:
        
        # Setup mock returns
        mock_input.return_value = "test_user"
        mock_button.return_value = True
        
        # Run function
        login_page()
        
        # Verify input fields were created
        assert mock_input.call_count >= 2  # Username and password fields
        mock_input.assert_any_call("Username", key="login_username")
        mock_input.assert_any_call("Password", type="password", key="login_password")

def test_sidebar(mock_session_state):
    """Test sidebar functionality"""
    # Set required session state
    mock_session_state.authenticated = True
    mock_session_state.username = "test_user"
    mock_session_state.menu = "Movies"
    
    with patch('streamlit.sidebar.title') as mock_title, \
         patch('streamlit.sidebar.selectbox') as mock_selectbox:
        
        # Setup mock return
        mock_selectbox.return_value = "Movies"
        
        # Run function
        sidebar()
        
        # Verify sidebar components
        mock_title.assert_called_once_with("Welcome, test_user")
        mock_selectbox.assert_called_once()

def test_set_background():
    """Test background setting functionality"""
    test_image_path = "/app/assets/background.png"
    
    # Mock the get_encoded_background function instead of open
    with patch('components.utils.get_encoded_background') as mock_get_encoded, \
         patch('streamlit.markdown') as mock_markdown:
        
        # Setup mock return
        mock_get_encoded.return_value = "test_encoded_content"
        
        # Run function
        set_background(test_image_path)
        
        # Verify function calls
        mock_get_encoded.assert_called_once_with(test_image_path)
        mock_markdown.assert_called_once()
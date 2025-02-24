import pytest
from components.utils import get_encoded_background, set_background
from unittest.mock import mock_open, patch

def test_get_encoded_background():
    """Test background image encoding"""
    test_image_content = b"test image content"
    mock_file = mock_open(read_data=test_image_content)
    
    with patch('builtins.open', mock_file):
        encoded = get_encoded_background("/test/path/image.png")
        assert isinstance(encoded, str)

def test_set_background_error_handling():
    """Test background setting error handling"""
    with patch('streamlit.error') as mock_error:
        with patch('builtins.open', side_effect=FileNotFoundError):
            set_background("/nonexistent/path/image.png")
            mock_error.assert_called_once()
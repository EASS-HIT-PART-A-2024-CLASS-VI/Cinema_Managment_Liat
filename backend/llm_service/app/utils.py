from typing import Dict, Any

def format_response(response: str) -> Dict[str, Any]:
    """Format the LLM response for the Cinema Management System."""
    return {
        "status": "success",
        "response": response
    }

def format_error(error: str) -> Dict[str, Any]:
    """Format error responses for the Cinema Management System."""
    return {
        "status": "error",
        "message": str(error)
    }

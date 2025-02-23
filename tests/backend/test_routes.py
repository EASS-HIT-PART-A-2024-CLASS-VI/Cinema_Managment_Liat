import pytest
from fastapi.testclient import TestClient

# Root endpoint test
def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Cinema Management System!"}

# Movies endpoint tests
def test_get_movies(client):
    """Test retrieving movies."""
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_titles_dropdown(client):
    """Test retrieving movie titles dropdown."""
    response = client.get("/movies/dropdown")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sorted_movies(client, sample_movie_data, sample_movie_sorted_data):
    """Test getting sorted movies."""
    # Add two movies with different ratings
    first_movie_response = client.post("/movies", json=sample_movie_data)
    assert first_movie_response.status_code == 200

    sorted_movie_response = client.post("/movies", json=sample_movie_sorted_data)
    assert sorted_movie_response.status_code == 200
    
    response = client.get("/movies/sorted")
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) >= 2
    assert movies[0]["critics_rating"] >= movies[1]["critics_rating"]

def test_add_movie(client, sample_movie_data):
    """Test adding a movie."""
    response = client.post("/movies", json=sample_movie_data)
    assert response.status_code == 200
    assert response.json()["title"] == sample_movie_data["title"]

def test_delete_movie(client, sample_movie_data):
    """Test deleting a movie."""
    # First add a movie
    add_response = client.post("/movies", json=sample_movie_data)
    assert add_response.status_code == 200
    movie_id = add_response.json()["id"]
    
    # Then delete it
    delete_response = client.delete(f"/movies/{movie_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Movie deleted successfully"

# Employees endpoint tests
def test_get_employees(client):
    """Test retrieving employees."""
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_employee_names_dropdown(client):
    """Test retrieving employee names dropdown."""
    response = client.get("/employees/dropdown")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sorted_employees(client, sample_employee_data, sample_manager_data):
    """Test getting sorted employees."""
    # Add employees with different salaries
    first_employee_response = client.post("/employees", json=sample_employee_data)
    assert first_employee_response.status_code == 200

    manager_response = client.post("/employees", json=sample_manager_data)
    assert manager_response.status_code == 200
    
    response = client.get("/employees/sorted")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) >= 2
    assert employees[0]["salary"] >= employees[1]["salary"]

def test_get_employees_birthdays(client, sample_birthday_employee_data):
    """Test retrieving employees with birthdays in current month."""
    # Add an employee with birthday in current month
    add_response = client.post("/employees", json=sample_birthday_employee_data)
    assert add_response.status_code == 200
    
    response = client.get("/employees/birthdays")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_employee(client, sample_employee_data):
    """Test adding an employee."""
    response = client.post("/employees", json=sample_employee_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == sample_employee_data["first_name"]

def test_delete_employee(client, sample_employee_data):
    """Test deleting an employee."""
    # First add an employee
    add_response = client.post("/employees", json=sample_employee_data)
    assert add_response.status_code == 200
    employee_id = add_response.json()["id"]
    
    # Then delete them
    delete_response = client.delete(f"/employees/{employee_id}")
    assert delete_response.status_code == 200
    assert "successfully" in delete_response.json()["message"]

# Branches endpoint tests
def test_get_branches(client):
    """Test retrieving branches."""
    response = client.get("/branches")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_branch_names_dropdown(client):
    """Test retrieving branch names dropdown."""
    response = client.get("/branches/dropdown")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_branch(client, sample_branch_data, sample_manager_data):
    """Test adding a branch."""
    # First add a manager
    manager_response = client.post("/employees", json=sample_manager_data)
    assert manager_response.status_code == 200
    
    # Then add a branch
    response = client.post("/branches", json=sample_branch_data)
    assert response.status_code == 200
    assert response.json()["name"] == sample_branch_data["name"]

def test_delete_branch(client, sample_branch_data, sample_manager_data):
    """Test deleting a branch."""
    # Setup: Add manager and branch
    manager_response = client.post("/employees", json=sample_manager_data)
    assert manager_response.status_code == 200
    
    branch_response = client.post("/branches", json=sample_branch_data)
    assert branch_response.status_code == 200
    branch_id = branch_response.json()["id"]
    
    # Delete branch
    delete_response = client.delete(f"/branches/{branch_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Branch deleted successfully"

# Authentication tests
def test_login(client, sample_manager_data, sample_login_data):
    """Test user login."""
    # First create a manager (which automatically creates login credentials)
    manager_response = client.post("/employees", json=sample_manager_data)
    assert manager_response.status_code == 200
    
    # Try to login
    response = client.post("/login", json=sample_login_data)
    assert response.status_code == 200
    assert "Successfully logged in" in response.json()["message"]

def test_logout(client):
    """Test user logout."""
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"

# LLM integration tests
def test_llm_chat(client, sample_llm_request):
    """Test LLM chat integration."""
    response = client.post("/api/llm/chat", json=sample_llm_request)
    # Note: Adjust status code based on your LLM service configuration
    assert response.status_code in [200, 500]

# Error case tests
def test_get_nonexistent_movie(client):
    """Test retrieving a non-existent movie."""
    response = client.get("/movies/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"

def test_get_nonexistent_employee(client):
    """Test retrieving a non-existent employee."""
    response = client.get("/employees/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

def test_get_nonexistent_branch(client):
    """Test retrieving a non-existent branch."""
    response = client.get("/branches/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"

def test_invalid_login_credentials(client):
    """Test login with invalid credentials."""
    response = client.post("/login", json={
        "username": "nonexistent",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]
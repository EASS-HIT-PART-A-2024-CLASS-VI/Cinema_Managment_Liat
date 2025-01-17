import requests
from fastapi.testclient import TestClient
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Backend Tests
@pytest.fixture(scope="module")
def backend_client():
    from app.backend.app.main import app
    client = TestClient(app)
    yield client

# Frontend Tests with Selenium
@pytest.fixture(scope="module")
def selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# Integration Test Fixtures
@pytest.fixture(scope="module")
def frontend_base_url():
    return "http://localhost:8501"

@pytest.fixture(scope="module")
def backend_base_url():
    return "http://localhost:8000"

# Movies Integration Test
def test_integration_movies(frontend_base_url, backend_base_url, selenium_driver):
    # Backend: Add a movie
    movie_data = {
        "title": "Inception",
        "genre": "Sci-Fi",
        "age_limit": False,
        "director": "Christopher Nolan",
        "duration_minutes": 148,
        "release_date": "2010-07-16",
        "critics_rating": 9.0
    }
    response = requests.post(f"{backend_base_url}/movies", json=movie_data)
    assert response.status_code == 200

    # Frontend: Verify Movie is Listed
    selenium_driver.get(frontend_base_url)
    time.sleep(2)

    # Interact with the "Movies" section
    movies_menu = selenium_driver.find_element(By.XPATH, "//select[@id='menu']")
    movies_menu.click()
    time.sleep(1)

    movies_action = selenium_driver.find_element(By.XPATH, "//input[@value='View Movies']")
    movies_action.click()
    time.sleep(2)

    # Verify that the added movie is displayed
    movie_titles = selenium_driver.find_elements(By.XPATH, "//select[@id='movie_titles']")
    assert any("Inception" in title.text for title in movie_titles)

    # Backend Cleanup: Delete the Movie
    movie_id = response.json()["id"]
    delete_response = requests.delete(f"{backend_base_url}/movies/{movie_id}")
    assert delete_response.status_code == 200

# Employees Integration Test
def test_integration_employees(frontend_base_url, backend_base_url, selenium_driver):
    # Backend: Add an employee
    employee_data = {
        "personal_id": "12345",
        "phone_number": "5551234567",
        "first_name": "John",
        "last_name": "Doe",
        "birth_year": "1985-05-15",
        "start_year": "2020-01-01",
        "role": "Cashier",
        "city": "Tel Aviv",
        "salary": 5000.0
    }
    response = requests.post(f"{backend_base_url}/employees", json=employee_data)
    assert response.status_code == 200

    # Frontend: Verify Employee is Listed
    selenium_driver.get(frontend_base_url)
    time.sleep(2)

    # Interact with the "Employees" section
    employees_menu = selenium_driver.find_element(By.XPATH, "//select[@id='menu']")
    employees_menu.click()
    time.sleep(1)

    employees_action = selenium_driver.find_element(By.XPATH, "//input[@value='View Employees']")
    employees_action.click()
    time.sleep(2)

    # Verify that the added employee is displayed
    employee_names = selenium_driver.find_elements(By.XPATH, "//select[@id='employee_names']")
    assert any("John Doe" in name.text for name in employee_names)

    # Backend Cleanup: Delete the Employee
    employee_id = response.json()["id"]
    delete_response = requests.delete(f"{backend_base_url}/employees/{employee_id}")
    assert delete_response.status_code == 200

# Branches Integration Test
def test_integration_branches(frontend_base_url, backend_base_url, selenium_driver):
    # Backend: Add a branch
    branch_data = {
        "name": "Downtown Cinema",
        "manager_id": "12345",
        "opening_time": "09:00:00",
        "closing_time": "23:00:00",
        "opening_year": "2015-06-01",
        "customer_service_phone": "5559876543"
    }
    response = requests.post(f"{backend_base_url}/branches", json=branch_data)
    assert response.status_code == 200

    # Frontend: Verify Branch is Listed
    selenium_driver.get(frontend_base_url)
    time.sleep(2)

    # Interact with the "Branches" section
    branches_menu = selenium_driver.find_element(By.XPATH, "//select[@id='menu']")
    branches_menu.click()
    time.sleep(1)

    branches_action = selenium_driver.find_element(By.XPATH, "//input[@value='View Branches']")
    branches_action.click()
    time.sleep(2)

    # Verify that the added branch is displayed
    branch_names = selenium_driver.find_elements(By.XPATH, "//select[@id='branch_names']")
    assert any("Downtown Cinema" in name.text for name in branch_names)

    # Backend Cleanup: Delete the Branch
    branch_id = response.json()["id"]
    delete_response = requests.delete(f"{backend_base_url}/branches/{branch_id}")
    assert delete_response.status_code == 200

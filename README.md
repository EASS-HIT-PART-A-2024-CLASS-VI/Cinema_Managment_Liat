# Welcome To Cinema Management System!

## Overview
The **Cinema Management System** is a comprehensive solution for managing and controlling data related to cinemas. Designed to simplify movie, employee, and branch management.

The backend, powered by **FastAPI**, ensures robust and secure API services. The frontend, built with **Streamlit**, provides a user-friendly interface.

## **Table of Contents**
1. [Technologies Used](#technologies-used)
2. [Project Features](#project-features)
3. [Project Structure](#project-structure)
4. [Endpoints (Backend)](#endpoints-backend)
5. [How to Run the Project](#how-to-run-the-project)

## Technologies Used
- **Backend**: Python 3.8, FastAPI (running on WSL).
- **Frontend**: Streamlit (running on WSL).
- **Database**: PostgreSQL.
- **Containerization**: Docker and Docker Compose.

## Project Features
### Backend
- **CRUD Operations**:
  - Manage movies, employees, and branches.
- **Login Functionality**:
  - Managers can log in using their name as a username.

### Frontend
- User-friendly interface built with Streamlit for:
  - Viewing and managing movies, employees, and branches.
  - Adding movies, employees, and branches.
  - Login for managers to access controlled functionalities.

## Project Structure

```plaintext
app/
├── backend/
│   ├── Dockerfile
│   └── app/
│       ├── __pycache__/
│       ├── crud.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── requirements.txt
│       └── schemas.py
├── docker-compose.yml
└── frontend/
    ├── Dockerfile
    ├── background.png
    └── frontend.py
```

---

## API Endpoints:

**General:**
Authentication:
- POST /login
  Description: Allows managers to log in by verifying their credentials.
  Request Body:
    {
      "username": "string",
      "password": "string"
    }
  Response: A success or failure message.

**Movies Endpoints:**
- GET /movies/dropdown
  Description: Fetches a list of movie titles for dropdown menus.
  Response: List of movie titles (strings).

- GET /movies
  Description: Retrieves all movies.
  Response: List of movies (schemas.Movie).

- GET /movies/{movie_id}
  Description: Retrieves a specific movie by its ID.
  Path Parameter: movie_id (integer).
  Response: A single movie (schemas.Movie).
  Error: 404 if the movie is not found.

- POST /movies
  Description: Adds a new movie to the database.
  Request Body: schemas.MovieCreate.
  Response: The created movie (schemas.Movie).

**Employees Endpoints:**
- GET /employees
  Description: Retrieves all employees.
  Response: List of employees (schemas.Employee).

- GET /employees/dropdown
  Description: Fetches a list of employee names for dropdown menus.
  Response: List of employee full names (strings).

- GET /employees/{employee_id}
  Description: Retrieves a specific employee by their ID.
  Path Parameter: employee_id (string).
  Response: A single employee (schemas.Employee).
  Error: 404 if the employee is not found.

- POST /employees
  Description: Adds a new employee to the database. If the role is "Manager," their credentials are added to the permissions table with a default password.
  Request Body: schemas.EmployeeCreate.
  Response: The created employee (schemas.Employee).

**Branches Endpoints:**
- GET /branches
  Description: Retrieves all branches.
  Response: List of branches (schemas.Branch).

- GET /branches/dropdown
  Description: Fetches a list of branch names for dropdown menus.
  Response: List of branch names (strings).

- GET /branches/{branch_id}
  Description: Retrieves a specific branch by its ID.
  Path Parameter: branch_id (integer).
  Response: A single branch (schemas.Branch).
  Error: 404 if the branch is not found.

- POST /branches
  Description: Adds a new branch to the database.
  Request Body: schemas.BranchCreate.
  Response: The created branch (schemas.Branch).

---
## **How to Run the Project**

### **Prerequisites:**
- Docker and Docker Compose installed.

### **Step 1: Clone the Repository**
```bash
git clone git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/Cinema_Managment_Liat.git
cd Cinema_Managment_Liat
```
### **Step 2: Build and Run Containers**
```bash
docker compose up --build
```
- The backend will be available at: [http://localhost:8000](http://localhost:8000)
- The frontend will be available at: [http://localhost:8501](http://localhost:8501)
### **Step 3: Use the Application**
- Open [http://localhost:8000](http://localhost:8000) in your browser.
- **Login :** Log in using the manager's first name as the username.
- **Navigate through the menu to access various sections such as Movies, Employees, and Branches:**
- **Manage Movies:** View, add, save new data.
- **Manage Employees:** View, add, save new data.
- **Manage Branches:** View, add, save new data.
---


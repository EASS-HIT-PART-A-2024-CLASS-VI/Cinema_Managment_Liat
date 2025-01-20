# Welcome to Cinema Management System!

## Overview
The **Cinema Management System** is a comprehensive platform designed to manage and streamline operations related to cinemas, including movies, employees, and branches. This system provides an easy-to-use interface and robust backend capabilities.

The backend is powered by **FastAPI**, ensuring secure and efficient API services, while the frontend is built with **Streamlit** for a user-friendly experience.
---
## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Endpoints](#endpoints)
5. [How to Run the Project](#how-to-run-the-project)

---

## Technologies Used
- **Backend**: Python 3.9, FastAPI (running on WSL).
- **Frontend**: Streamlit (running on WSL).
- **Database**: PostgreSQL.
- **Authentication**: bcrypt for password hashing.
- **Containerization**: Docker and Docker Compose.

---

## Features
### Backend
- **CRUD Operations**: Manage movies, employees, and branches.
- **Login Functionality**: Managers can log in using their first name as a username.

### Frontend
- User-friendly Streamlit interface for:
  - Viewing, adding, and deleting movies, employees, and branches.
  - Secure manager login.

---

## Project Structure
```plaintext
.
├── README.md
├── app.mp4
├── backend
│   ├── Dockerfile
│   └── app
│       ├── __pycache__
│       │   ├── crud.cpython-39.pyc
│       │   ├── database.cpython-39.pyc
│       │   ├── main.cpython-39.pyc
│       │   ├── models.cpython-39.pyc
│       │   └── schemas.cpython-39.pyc
│       ├── crud.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── requirements.txt
│       └── schemas.py
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── background.png
│   ├── branchesback.png
│   ├── employeeback.png
│   ├── frontend.py
│   └── moviesback.png
└── integration_test.py
```
---

## Endpoints

### Authentication
- **POST /login**: Allows managers to log in by verifying their credentials.
  - Request Body:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - Response: A success or failure message.

### Movies Endpoints
- **GET /movies/dropdown**: Fetches a list of movie titles for dropdown menus.
- **GET /movies**: Retrieves all movies.
- **GET /movies/{movie_id}**: Retrieves a specific movie by ID.
- **POST /movies**: Adds a new movie to the database.
  - Request Body: schemas.MovieCreate.
- **DELETE /movies/{movie_id}**: Deletes a movie by ID.

### Employees Endpoints
- **GET /employees**: Retrieves all employees.
- **GET /employees/dropdown**: Fetches a list of employee names for dropdown menus.
- **GET /employees/{employee_id}**: Retrieves a specific employee by ID.
- **POST /employees**: Adds a new employee to the database. If the role is "Manager," credentials are added to the permissions table.
  - Request Body: schemas.EmployeeCreate.
- **DELETE /employees/{employee_id}**: Deletes an employee by ID.

### Branches Endpoints
- **GET /branches**: Retrieves all branches.
- **GET /branches/dropdown**: Fetches a list of branch names for dropdown menus.
- **GET /branches/{branch_id}**: Retrieves a specific branch by ID.
- **POST /branches**: Adds a new branch to the database.
  - Request Body: schemas.BranchCreate.
- **DELETE /branches/{branch_id}**: Deletes a branch by ID.

---

## How to Run the Project

### Prerequisites
- Docker and Docker Compose installed.

### Step 1: Clone the Repository
```bash
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/Cinema_Managment_Liat.git
cd Cinema_Managment_Liat
```

### Step 2: Build and Run Containers
```bash
docker compose up --build
```
- The backend will be available at: [http://localhost:8000](http://localhost:8000)
- The frontend will be available at: [http://localhost:8501](http://localhost:8501)

### Step 3: Use the Application
- Open the application in your browser:
  - Backend: [http://localhost:8000](http://localhost:8000)
  - Frontend: [http://localhost:8501](http://localhost:8501)
- **Login**:
  - Use the manager's first name as the username.
  - Default password: `Aa123456`.
- Navigate through the menu to:
  - **Manage Movies**: View, add, and delete movies.
  - **Manage Employees**: View, add, and delete employees (A manager can't be deleted if he is connected to a branch).
  - **Manage Branches**: View, add, and delete branches.

---


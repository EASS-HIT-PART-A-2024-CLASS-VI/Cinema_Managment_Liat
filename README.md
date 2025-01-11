# Welcome To Cinema Management System!

## Overview
The **Cinema Management System** is a comprehensive solution for managing and controlling data related to cinemas. Designed with scalability and user-friendliness in mind, this application allows administrators to efficiently manage movies, employees, and branches.

The backend, powered by **FastAPI**, ensures robust and secure API services. The frontend, built with **Streamlit**, provides a clean and intuitive user interface for interacting with the system. Data is stored in a **PostgreSQL database**, and the project is containerized using **Docker**, ensuring seamless deployment and compatibility across environments.

## Technologies Used
<<<<<<< HEAD
- **Backend**: Python 3.8, FastAPI (running on WSL).
- **Frontend**: Streamlit (running on WSL).
- **Database**: PostgreSQL.
- **Containerization**: Docker.

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
app
├── backend/
│   ├── Dockerfile
│   └── app/
│       ├── __pycache__/
│       │   ├── crud.cpython-39.pyc
│       │   ├── database.cpython-39.pyc
│       │   ├── main.cpython-39.pyc
│       │   ├── models.cpython-39.pyc
│       │   └── schemas.cpython-39.pyc
│       ├── crud.py         # Backend CRUD operations
│       ├── database.py     # Database connection setup
│       ├── main.py         # FastAPI application entry point
│       ├── models.py       # Database models
│       ├── requirements.txt # Python dependencies
│       └── schemas.py      # Pydantic schemas
├── docker-compose.yml      # Multi-container orchestration
└── frontend/
    ├── Dockerfile
    └── frontend.py         # Streamlit frontend


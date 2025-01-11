# Welcome To Cinema Management System!

## Overview
The **Cinema Management System** is a comprehensive solution for managing and controlling data related to cinemas. Designed to simplify movie, employee, and branch management.

The backend, powered by **FastAPI**, ensures robust and secure API services. The frontend, built with **Streamlit**, provides a user-friendly interface.

## Technologies Used
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



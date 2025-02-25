# Welcome to Cinema Management System 📽️
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-blue?style=for-the-badge&logo=google&logoColor=white)](https://gemini.google.com/chat)

A microservices-based cinema management system designed for efficient movie scheduling, employee management, and branch operations, with integrated AI-powered assistance.

The **Cinema Management System** is a full-stack application designed to streamline movie scheduling, employee management, and branch operations. Featuring a modern Streamlit frontend, a FastAPI backend, and cutting-edge technologies like LLM integration, this system provides intelligent assistance for cinema operations. Dockerized for seamless deployment, the application is built on a microservices architecture to ensure scalability and flexibility.

## 📋 Table of Contents
- [Features](#-features)
- [Project Architecture](#️-project-architecture)
- [Demo](#-demo)
- [Prerequisites](#️-prerequisites)
- [Setting up the Project](#️-setting-up-the-project)
- [Docker Deployment](#-docker-deployment)
- [First-Time Setup](#-first-time-setup)
- [API Endpoints](#-api-endpoints)
- [Frontend](#️-frontend)
- [LLM Microservice Features](#-llm-microservice-features)
- [Port Configuration](#️-port-configuration)
- [Testing](#-testing)
- [Author](#-author)

## 🚀 Features
- **Movie Scheduling:** Efficiently manage screening times across multiple branches.
- **Employee Management:** Handle staff details, roles, and schedules seamlessly.
- **Branch Operations:** Oversee branch opening hours, managers, and customer service contacts.
- **LLM-Powered Assistance:** Get intelligent support for cinema operations with AI integration.
- **Microservices Architecture:** Modular FastAPI backend ensures scalability and maintainability.
- **Streamlit Frontend:** Intuitive and responsive UI for effortless management.
- **Docker Support:** Seamless deployment using Docker Compose for a hassle-free setup.

## 🗂️ Project Architecture

<img src="frontend/assets/architecture_diagram.png" alt="Architecture Diagram" width="65%">

```plaintext
.
└── app
    ├── README.md
    ├── __init__.py
    ├── backend
    │   ├── Dockerfile
    │   ├── app
    │   │   ├── crud.py
    │   │   ├── database.py
    │   │   ├── main.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   ├── requirements.txt
    │   │   ├── test_cinema.db
    │   │   └── tests/
    │   └── llm_service
    │       ├── Dockerfile
    │       ├── __init__.py
    │       ├── app
    │       │   ├── config/settings.py
    │       │   ├── gemini.py
    │       │   ├── main.py
    │       │   ├── prompt.py
    │       │   └── utils.py
    │       └── requirements.txt
    ├── docker-compose.yml
    ├── frontend
    │   ├── Dockerfile
    │   ├── app.py
    │   ├── assets/
    │   ├── components/
    │   │   ├── login.py
    │   │   ├── sidebar.py
    │   │   └── utils.py
    │   ├── pages/
    │   │   ├── branches.py
    │   │   ├── employees.py
    │   │   └── movies.py
    │   ├── requirements.txt
    │   ├── setup.py
    │   └── tests/
    └── tests/
```
---

## 🎥 Demo

<a href="https://youtu.be/H_tabs6GUPk" target="_blank">
  <img 
    src="frontend/assets/video_cover.png" 
    alt="Cinema Managment Demo" 
    width="100%"
  />
</a>

---
### 🛠️ Prerequisites
- Docker and Docker Compose installed
- Python 3.9+
- Git

## 🏗️ **Setting up the Project**

To enable **Google Gemini AI**, you must create an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

Then, create a `.env` file in the root directory and fill it with:
```bash
    GOOGLE_API_KEY=<YOUR_API_KEY>'
``` 

Ensure `.env` is **excluded from version control** by adding it to `.gitignore`.

Clone the repository:
```bash
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/Cinema_Managment_Liat.git
cd Cinema_Managment_Liat
```   
## 🐳 Docker Deployment

To deploy all services, run:

`docker-compose up --build` 

This will start **all microservices** (Backend, Frontend, Database, and AI Service).

Once running:

- Frontend: `http://localhost:8501`
- Backend : `http://localhost:8000`
- Swagger LLM Service: `http://localhost:8001/docs` 

## 🔑 First-Time Setup
Since the database is initially empty, you need to create a manager account to log in.

After starting all services with Docker Compose, create a manager using the following curl command:

```bash
curl -X POST http://localhost:8000/employees \
  -H "Content-Type: application/json" \
  -d '{
    "personal_id": "123456789",
    "phone_number": "0501234567",
    "first_name": "Admin",
    "last_name": "Manager",
    "birth_year": "1990-01-01",
    "start_year": "2020-01-01",
    "role": "Manager",
    "city": "Test City",
    "salary": 50000.0
  }'
```

Alternatively, you can use Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs) to send the POST request to the `/employees` endpoint with the above JSON data.

### **Login:**
- Use the manager's first name (e.g., **"Admin"**) as the username.
- **Default password:** `Aa123456`

---

## 📚 API Endpoints
The FastAPI backend provides RESTful endpoints for managing the system:

### 🔑 Authentication Endpoints

#### **POST `/login`** - Allows managers to log in by verifying their credentials.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```
#### **POST `/logout`** - Log out a user from the system.
---
### 🎮 Movies Endpoints

- **GET** `/movies` - Retrieve all movies
- **POST** `/movies` - Add a new movie
- **DELETE** `/movies/{movie_id}` - Delete a movie
- **GET** `/movies/sorted` - Get movies sorted by critics' ratings
- **GET** `/movies/dropdown` - Retrieve a list of movie titles
---
### 👥 Employees Endpoints

- **GET** `/employees` - Retrieve all employees
- **POST** `/employees` - Add a new employee
- **DELETE** `/employees/{employee_id}` - Delete an employee
- **GET** `/employees/sorted` - Get employees sorted by salary
- **GET** `/employees/birthdays` - Retrieve employees with birthdays in the current month
- **GET** `/employees/dropdown` - Retrieve a list of employee names
---
### 🏢 Branches Endpoints

- **GET** `/branches` - Retrieve all branches
- **POST** `/branches` - Add a new branch
- **DELETE** `/branches/{branch_id}` - Delete a branch
- **GET** `/branches/dropdown` - Retrieve a list of branch names
---
### 🎭 Schedule (Not an Endpoint)
Each branch has a screening schedule that includes:

- Movie title
- Hall number
- Showtime
- Duration

Schedules are stored per branch and update when a movie is deleted.

---
## 🖥️ Frontend

The Streamlit frontend provides an intuitive interface for managing all cinema operations:

### 🔑 Authentication
- Secure manager login with password protection
- Dynamic session management for secure access
- Role-based access control (RBAC) limited to managers

### 🎬 Movie Management
- Browse complete movie inventory with detailed information
- Add new movies with comprehensive metadata
- Sort movies by critics' ratings for quality assessment
- Delete outdated movies with automatic schedule cleanup

### 👥 Employee Management
- View employee directory with comprehensive details
- Add new staff members with role-specific configurations
- Track employee birthdays with automatic monthly highlights
- Sort employees by salary for payroll management

### 🏢 Branch Management
- Track all cinema locations with operational details
- Register new branches with manager assignment
- Configure branch operating hours and contact information
- Manage branch-specific screening schedules

### 🎭 Schedule Management
- Interactive screening scheduler with visual timetables
- Conflict detection to prevent scheduling overlaps
- Hall-specific program management across multiple days
- Automatic cleanup when movies are removed from system

### 🤖 AI Assistant
- Built-in chatbot powered by Google Gemini AI
- Get assistance with system navigation and operations
- Access contextual help for specific management tasks
- Receive guidance on best practices for cinema management

### 🎨 User Experience
- Dynamic theming with custom backgrounds for each section
- Responsive layout that adapts to different screen sizes
- Intuitive navigation through sidebar menu system
- Consistent styling with clear visual hierarchy

## 🚫 General System Restrictions
- **Only managers** can access the system.
- Employees **cannot log in** or modify system data.

---

## 🤖 LLM Microservice Features

The **Cinema Management System** integrates **Google Gemini AI** (model: gemini-1.5-pro) to provide intelligent assistance for cinema operations. The LLM offers **helpful guidance** and **operational instructions** through a dedicated microservice, enhancing the user experience with AI-powered support.

### 🎮 Movie Management Guidance
- Explain how to add, view, and delete movies in the system
- Provide guidance on sorting and filtering movie lists
- Offer general information about movie management practices

### 👥 Employee Management Guidance
- Guide users on how to add and remove employees
- Explain the process for viewing employee information
- Provide instructions for accessing birthday lists and sorted employee views

### 🏢 Branch Management Guidance
- Explain branch management functionality
- Guide users on adding new branches and required information
- Provide instructions for managing branch operations

### 🎭 Screening Schedule Guidance
- Explain the process of scheduling movies across branches
- Provide best practices for managing screenings and avoiding conflicts
- Offer instructions on maintaining and updating screening schedules

### 📌 System Navigation Assistance
- Help users navigate between different system sections
- Explain UI elements and their functions
- Provide troubleshooting steps for common issues

### 🔧 Technical Implementation
- Simple REST API endpoint at `/chat` for processing user questions
- System prompt focused exclusively on cinema management topics
- No direct database access - provides only general guidance
- Environment variable configuration via `GOOGLE_API_KEY`

📌 **The LLM provides helpful instructions and explanations about system functionality without accessing or modifying actual data.**
## 🛠️ Port Configuration

### **Frontend**
- **Port:** `8501`
- **URL:** [http://localhost:8501](http://localhost:8501)

### **Backend API**
- **Port:** `8000`
- **URL:** [http://localhost:8000](http://localhost:8000)
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

### **LLM Chatbot**
- **Port:** `8001`
- **URL:** [http://localhost:8001](http://localhost:8001)
- **Swagger UI:** [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 🧪 Testing

### **Backend Tests**
Run tests from the project root:

# Run all backend tests inside the Docker container

```bash
docker-compose exec backend bash -c "PYTHONPATH=/app pytest"
```

The backend tests cover:
- API endpoints functionality
- CRUD operations
- Authentication
- Data validation
- Error handling

### **Frontend Tests**

Run tests from the frontend directory:

```bash
docker-compose exec frontend bash -c "cd /app && pytest tests/"
```

Frontend tests validate:
- Component rendering
- Page navigation
- User interactions
- API integration

### **Running Tests During Development**
For local testing during development:

```bash
# Navigate to the app directory
cd app

# Run backend tests
docker-compose exec backend bash -c "PYTHONPATH=/app pytest"
```
These testing commands ensure all tests run in the appropriate Docker environment with the correct paths and dependencies.
---
## 👨‍💻 Author

- **Name:** Liat Simhayev
- **GitHub:** [liatsimhayev](https://github.com/liatsimhayev)

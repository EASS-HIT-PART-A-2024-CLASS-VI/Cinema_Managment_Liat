# Welcome to Cinema Management System 📽️
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
  [![Gemini AI](https://img.shields.io/badge/Gemini-AI-blue?style=for-the-badge&logo=google&logoColor=white)](https://gemini.google.com/chat)
</div>


  A microservices-based cinema management system designed for efficient movie scheduling, employee management, and branch operations, with integrated AI-powered assistance.
The **Cinema Management System** is a full-stack application designed to streamline movie scheduling, employee management, and branch operations. Featuring a modern Streamlit frontend, a FastAPI backend, and cutting-edge technologies like LLM integration, this system provides intelligent assistance for cinema operations. Dockerized for seamless deployment, the application is built on a microservices architecture to ensure scalability and flexibility

---
## 🚀 Features
- **Movie Scheduling:** Efficiently manage screening times across multiple branches.
- **Employee Management:** Handle staff details, roles, and schedules seamlessly.
- **Branch Operations:** Oversee branch opening hours, managers, and customer service contacts.
- **LLM-Powered Assistance:** Get intelligent support for cinema operations with AI integration.
- **Microservices Architecture:** Modular FastAPI backend ensures scalability and maintainability.
- **Streamlit Frontend:** Intuitive and responsive UI for effortless management.
- **Docker Support:** Seamless deployment using Docker Compose for a hassle-free setup.
---
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

### Prerequisites
- Docker and Docker Compose installed 🐳

## 🛠️ Setting Up the Project
To use the LLM-powered suggestions feature, you need to provide an API key for Google Gemini AI.
1. Visit [Google AI Studio](https://aistudio.google.com/apikey) to obtain your API key.
2. Create a `.env` file in the root directory (the folder that contains `backend/` and `frontend/`) and add the following line, replacing `<YOUR_API_KEY>` with your actual key:

   ```bash
   echo 'GOOGLE_API_KEY=<YOUR_API_KEY>' > .env
   ```
3. Ensure the .env file is not accidentally committed to version control by adding it to .gitignore.

### 💻 Running 

### Step 1: Clone the Repository
```bash
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/Cinema_Managment_Liat.git
cd Cinema_Managment_Liat
```
### Step 2: Build and Run Containers
```bash
docker compose up --build
```
- FastAPI backend: http://localhost:8000
- Streamlit frontend: http://localhost:8501
- PostgreSQL database connected via Docker network

- **Login**:
  - Use the manager's first name as the username.
  - Default password: `Aa123456`.

---
## 📖 API Endpoints
The FastAPI backend provides RESTful endpoints for managing the system:

### 🔑 Authentication Endpoints
- **`POST /login`** - Allows managers to log in by verifying their credentials.
  - Request Body:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
- **`POST /logout`** - Log out a user from the system.

### 🎬 Movies Endpoints
- **`GET /movies`** - Retrieve all movies
- **`POST /movies`** - Add a new movie
- **`DELETE /movies/{movie_id}`** - Delete a movie
- **`GET /movies/sorted`** - Get movies sorted by critics' ratings
- **`GET /movies/dropdown`** - Retrieve a list of movie titles

### 👥 Employees Endpoints
- **`GET /employees`** - Retrieve all employees
- **`POST /employees`** - Add a new employee
- **`DELETE /employees/{employee_id}`** - Delete an employee
- **`GET /employees/sorted`** - Get employees sorted by salary
- **`GET /employees/birthdays`** - Retrieve employees with birthdays in the current month
- **`GET /employees/dropdown`** - Retrieve a list of employee names

### 🏢 Branches Endpoints
- **`GET /branches`** - Retrieve all branches
- **`POST /branches`** - Add a new branch
- **`DELETE /branches/{branch_id}`** - Delete a branch
- **`GET /branches/dropdown`** - Retrieve a list of branch names

### 🎭 Schedule (Not an Endpoint)
Each branch has a **screening schedule** that includes:
- **Movie title**
- **Hall number**
- **Showtime**
- **Duration**  
Schedules are **stored per branch** and update when a movie is deleted.

📌 **API Documentation**: Available at [`http://localhost:8000/docs`](http://localhost:8000/docs)


## 🤖 LLM Microservice Features

The **Cinema Management System** integrates **Google Gemini AI** to assist with various management tasks. The LLM provides **intelligent guidance** and **operational support** for the following features:

### 🎬 **Movie Management**
- Retrieve movie details, including **genre, director, duration, and ratings**.
- Get **sorted movie lists** based on critics' ratings.
- Guide users on how to **add or delete movies** in the system.

### 👥 **Employee Management**
- Retrieve a **list of all employees** with relevant details.
- Provide guidance on **adding new employees** with necessary information.
- Retrieve **employees sorted by salary**.
- Retrieve a **list of employees with birthdays** in the current month.

### 🏢 **Branch Management**
- Retrieve **all cinema branch details**.
- Guide users on how to **add or delete branches**.
- Provide **customer service contact details** for each branch.

### 🎭 **Screening Schedule Management**
- Guide users on how to **assign movies to screening times** in different branches.
- Prevent **scheduling conflicts** based on **movie duration and branch hours**.
- Assist with **managing existing screenings** in the **Branch Management** section.

### 📌 **System Navigation Assistance**
- Provide **step-by-step guidance** on using the system, including:
  - Switching between **Movies, Employees, and Branches** sections.
  - Using the **sidebar for filtering and sorting options**.
  - Accessing **employee birthday lists** via the **"Birthdays 🎂"** button.
  - Managing **screenings** via the **"Manage Screenings 🎬"** button.

### 🚫 **General System Restrictions**
- **Only managers** can access the system.
- Employees **cannot log in** or modify system data.

📌 **The LLM ensures all responses are professional, accurate, and strictly related to cinema management.**

 ## Port Configuration

### Frontend
- **Port:** 3000
- **URL:** http://localhost:3000

### Backend API
- **Port:** 8000
- **URL:** http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs


### LLM Chatbot
- **Port:** 8001
- **URL:** http://localhost:8001
- **Swagger UI**: http://localhost:8001/docs

## 👨‍💻 Author

- **Name:** Liat Simhayev 
- **GitHub:** [liatsimhayev](https://github.com/liatsimhayev)

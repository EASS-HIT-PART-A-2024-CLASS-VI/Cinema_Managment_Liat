import streamlit as st
import requests
import datetime

# API base URL
BASE_URL = "http://backend:8000"

st.title("Cinema Management System")

# Navigation Menu
menu = st.sidebar.selectbox("Menu", ["Movies", "Employees", "Branches"])

# Helper function to clear inputs by rerunning the app
def clear_inputs():
    st.session_state.clear()

# Movies Section
if menu == "Movies":
    st.header("Movies Management")
    action = st.radio("Choose Action:", ["View Movies", "Add Movie"])

    if action == "View Movies":
        st.subheader("All Movies")
        try:
            response = requests.get(f"{BASE_URL}/movies")
            if response.status_code == 200:
                movies = response.json()
                if movies:
                    for movie in movies:
                        st.write(f"Title: {movie['title']}, Genre: {movie['genre']}, Director: {movie['director']}")
                else:
                    st.info("No movies found.")
            else:
                st.error(f"Failed to fetch movies: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    elif action == "Add Movie":
        st.subheader("Add a New Movie")
        movie_name = st.text_input("Movie Name", key="movie_name")
        genre = st.selectbox(
            "Genre",
            [
                "Comedy", "Romance", "Action", "Horror", "Sci-Fi",
                "Fantasy", "Thriller", "Drama", "Mystery", "Documentary"
            ],
            key="genre"
        )
        age_restriction = st.selectbox("Age Restriction", [True, False], key="age_restriction")
        director = st.text_input("Director Name", key="director")
        duration = st.number_input("Duration (minutes)", min_value=1, step=1, key="duration")
        release_date = st.date_input("Release Date", min_value=datetime.date(1970, 1, 1), key="release_date")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Movie"):
                movie_data = {
                    "title": st.session_state.movie_name,
                    "genre": st.session_state.genre,
                    "age_limit": st.session_state.age_restriction,
                    "director": st.session_state.director,
                    "duration_minutes": st.session_state.duration,
                    "release_date": str(st.session_state.release_date),
                    "critics_rating": 5.0  # Default rating
                }
                response = requests.post(f"{BASE_URL}/movies", json=movie_data)
                if response.status_code == 200:
                    st.success("Movie added successfully!")
                else:
                    st.error(f"Failed to add movie: {response.text}")
        with col2:
            if st.button("Clear"):
                clear_inputs()

# Employees Section
elif menu == "Employees":
    st.header("Employees Management")
    action = st.radio("Choose Action:", ["View Employees", "Add Employee"])

    if action == "View Employees":
        st.subheader("All Employees")
        try:
            response = requests.get(f"{BASE_URL}/employees")
            if response.status_code == 200:
                employees = response.json()
                for employee in employees:
                    st.write(employee)
            else:
                st.error(f"Failed to fetch employees: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    elif action == "Add Employee":
        st.subheader("Add a New Employee")
        emp_id = st.text_input("Employee ID", key="emp_id")
        phone_number = st.text_input("Phone Number", key="phone_number")
        first_name = st.text_input("First Name", key="first_name")
        last_name = st.text_input("Last Name", key="last_name")
        year_of_birth = st.date_input("Year of Birth", min_value=datetime.date(1970, 1, 1), key="birth_year")
        year_of_employment = st.date_input("Year of Employment", min_value=datetime.date(1970, 1, 1), key="start_year")
        role = st.selectbox(
            "Role",
            [
                "Cashier", "Canteen Seller", "Warehouse Worker",
                "Customer Center Worker", "Ticket Seller", "Manager"
            ],
            key="role"
        )
        city_of_residence = st.text_input("City of Residence", key="city")
        salary = st.number_input("Salary", min_value=0, step=1, key="salary")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Employee"):
                if not st.session_state.phone_number.isdigit():
                    st.error("Phone number must contain only digits.")
                else:
                    employee_data = {
                        "personal_id": st.session_state.emp_id,
                        "phone_number": st.session_state.phone_number,
                        "first_name": st.session_state.first_name,
                        "last_name": st.session_state.last_name,
                        "birth_year": str(st.session_state.birth_year),
                        "start_year": str(st.session_state.start_year),
                        "role": st.session_state.role,
                        "city": st.session_state.city,
                        "salary": st.session_state.salary
                    }
                    response = requests.post(f"{BASE_URL}/employees", json=employee_data)
                    if response.status_code == 200:
                        st.success("Employee added successfully!")
                    else:
                        st.error(f"Failed to add employee: {response.text}")
        with col2:
            if st.button("Clear"):
                clear_inputs()

# Branches Section
elif menu == "Branches":
    st.header("Branches Management")
    action = st.radio("Choose Action:", ["View Branches", "Add Branch"])

    if action == "View Branches":
        st.subheader("All Branches")
        try:
            response = requests.get(f"{BASE_URL}/branches")
            if response.status_code == 200:
                branches = response.json()
                for branch in branches:
                    st.write(branch)
            else:
                st.error(f"Failed to fetch branches: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    elif action == "Add Branch":
        st.subheader("Add a New Branch")
        branch_name = st.text_input("Branch Name", key="branch_name")
        manager_id = st.text_input("Manager ID", key="manager_id")
        opening_time = st.time_input("Opening Time", key="opening_time")
        closing_time = st.time_input("Closing Time", key="closing_time")
        opening_year = st.date_input("Opening Year", min_value=datetime.date(1970, 1, 1), key="opening_year")
        customer_service_phone = st.text_input("Customer Service Phone", key="customer_service_phone")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Branch"):
                if not st.session_state.customer_service_phone.isdigit():
                    st.error("Phone number must contain only digits.")
                else:
                    branch_data = {
                        "name": st.session_state.branch_name,
                        "manager_id": st.session_state.manager_id,
                        "opening_time": str(st.session_state.opening_time),
                        "closing_time": str(st.session_state.closing_time),
                        "opening_year": str(st.session_state.opening_year),
                        "customer_service_phone": st.session_state.customer_service_phone
                    }
                    response = requests.post(f"{BASE_URL}/branches", json=branch_data)
                    if response.status_code == 200:
                        st.success("Branch added successfully!")
                    else:
                        st.error(f"Failed to add branch: {response.text}")
        with col2:
            if st.button("Clear"):
                clear_inputs()


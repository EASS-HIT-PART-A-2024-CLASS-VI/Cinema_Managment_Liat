import streamlit as st
import requests

# API base URL
BASE_URL = "http://localhost:8000"

st.title("Cinema Management System")

# Navigation Menu
menu = st.sidebar.selectbox("Menu", ["Movies", "Employees", "Branches"])

if menu == "Movies":
    st.header("Movies Management")
    action = st.radio("Choose Action:", ["View Movies", "Add Movie"])
    
    if action == "View Movies":
        st.subheader("All Movies")
        response = requests.get(f"{BASE_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            for movie in movies:
                st.write(movie)
        else:
            st.error("Failed to fetch movies.")
    
    elif action == "Add Movie":
        st.subheader("Add a New Movie")
        movie_name = st.text_input("Movie Name")
        genre = st.text_input("Genre")
        age_restriction = st.selectbox("Age Restriction", [True, False])
        director = st.text_input("Director Name")
        duration = st.number_input("Duration (minutes)", min_value=1, step=1)
        release_date = st.date_input("Release Date")
        
        if st.button("Save Movie"):
            movie_data = {
                "name": movie_name,
                "genre": genre,
                "age_restriction": age_restriction,
                "director": director,
                "duration": duration,
                "release_date": str(release_date)
            }
            response = requests.post(f"{BASE_URL}/movies", json=movie_data)
            if response.status_code == 200:
                st.success("Movie added successfully!")
            else:
                st.error("Failed to add movie.")

elif menu == "Employees":
    st.header("Employees Management")
    action = st.radio("Choose Action:", ["View Employees", "Add Employee"])
    
    if action == "View Employees":
        st.subheader("All Employees")
        response = requests.get(f"{BASE_URL}/employees")
        if response.status_code == 200:
            employees = response.json()
            for employee in employees:
                st.write(employee)
        else:
            st.error("Failed to fetch employees.")
    
    elif action == "Add Employee":
        st.subheader("Add a New Employee")
        emp_id = st.text_input("Employee ID")
        phone_number = st.text_input("Phone Number")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        year_of_birth = st.date_input("Year of Birth")
        year_of_employment = st.date_input("Year of Employment")
        role = st.selectbox("Role", ["Cashier", "Canteen Seller", "Warehouse Worker", "Customer Center Worker", "Ticket Seller"])
        city_of_residence = st.text_input("City of Residence")
        salary = st.number_input("Salary", min_value=0, step=1)
        
        if st.button("Save Employee"):
            employee_data = {
                "id": emp_id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "year_of_birth": str(year_of_birth),
                "year_of_employment": str(year_of_employment),
                "role": role,
                "city_of_residence": city_of_residence,
                "salary": salary
            }
            response = requests.post(f"{BASE_URL}/employees", json=employee_data)
            if response.status_code == 200:
                st.success("Employee added successfully!")
            else:
                st.error("Failed to add employee.")


import streamlit as st
import requests
import base64
import datetime

# API base URL
BASE_URL = "http://backend:8000"

# Function to encode an image for use as a background
@st.cache_data
def get_encoded_background(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def set_background(image_path):
    """
    Apply a full-page background image dynamically to cover the entire page,
    including the sidebar and header. All text remains styled as white.
    """
    try:
        encoded_string = get_encoded_background(image_path)
        st.markdown(
            f"""
            <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: white !important;
            }}
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .block-container {{
                padding: 2rem;
                color: white !important;
            }}
            header {{
                background: transparent !important;
                color: white !important;
            }}
            .stSidebar {{
                background-color: black !important;
                color: white !important;
            }}
            .stSidebar .css-1d391kg {{
                color: white !important;
            }}
            label {{
                color: white !important;
                font-size: 18px;
            }}
            .stButton>button {{
                background-color: black !important;
                color: white !important;
                font-weight: bold;
                border-radius: 5px;
                border: none;
                padding: 10px 20px;
            }}
            input, select, textarea {{
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid white !important;
                font-size: 16px;
            }}
            input[disabled], select[disabled], textarea[disabled] {{
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid white !important;
                opacity: 1 !important; /* Fix opacity issues for disabled fields */
            }}
            .stRadio > div {{
                color: white !important; /* Ensure radio buttons are styled */
            }}
            .stRadio > div > label {{
                color: white !important;
                font-size: 16px;
                font-weight: bold;
            }}
            [data-baseweb="select"] > div, [data-testid="stTimeInput"] > div {{
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid white !important;
                font-size: 16px;
                border-radius: 5px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("Background image not found. Please check the file path.")

# Initialize session state
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("menu", "Movies")  # Default menu

# Login Page
def login_page():
    """
    Render the login page with its specific background and login functionality.
    """
    set_background("/app/background.png")

    st.markdown('<h1 style="color:white;">Cinema Management System - Login</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color:white;">Please log in to access the system</h3>', unsafe_allow_html=True)

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not username or not password:
            st.error("Both fields are required!")
        else:
            try:
                response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
                if response.status_code == 200:
                    st.success("Login successful!")
                    st.session_state.authenticated = True
                    st.session_state.username = username
                elif response.status_code == 401:
                    st.error("Invalid username or password.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
# Main Application
def main_app():
    """
    Render the main application, dynamically setting backgrounds based on the selected menu.
    """
    # Set dynamic backgrounds based on menu selection
    if st.session_state.get("menu") == "Movies":
        set_background("/app/moviesback.png")  # Movies background
    elif st.session_state.get("menu") == "Employees":
        set_background("/app/employeeback.png")  # Employees background 
    elif st.session_state.get("menu") == "Branches":
        set_background("/app/branchesback.png")  # Branches background

    # Sidebar content
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    menu = st.sidebar.selectbox("Menu", ["Movies", "Employees", "Branches"], key="menu")

    # Movies Section
    if menu == "Movies":
        st.header("Movies Management")
        action = st.radio("Choose Action:", ["View Movies", "Add Movie"], key="movie_action")

        if action == "View Movies":
            st.subheader("View Movie Details")
            try:
                # Fetch movie titles for dropdown
                titles_response = requests.get(f"{BASE_URL}/movies/dropdown")
                if titles_response.status_code == 200:
                    movie_titles = titles_response.json()
                else:
                    st.error("Failed to fetch movie titles.")
                    return

                # Select a movie title
                selected_title = st.selectbox("Select a Movie", movie_titles, key="selected_movie")

                # Fetch all movie details
                details_response = requests.get(f"{BASE_URL}/movies")
                if details_response.status_code == 200:
                    movies = details_response.json()
                    movie = next((m for m in movies if m["title"] == selected_title), None)
                else:
                    st.error("Failed to fetch movie details.")
                    return

                if movie:
                    # Display movie details including critics rating
                    st.text_input("Title", value=movie["title"], disabled=True)
                    st.text_input("Genre", value=movie["genre"], disabled=True)
                    st.text_input("Director", value=movie["director"], disabled=True)
                    st.text_input("Age Restriction", value=str(movie["age_limit"]), disabled=True)
                    st.text_input("Duration (minutes)", value=str(movie["duration_minutes"]), disabled=True)
                    st.text_input("Release Date", value=movie["release_date"], disabled=True)
                    st.text_input("Critics Rating", value=str(movie["critics_rating"]), disabled=True)
                    
                    if st.button("Delete Movie"):
                        try:
                            delete_response = requests.delete(f"{BASE_URL}/movies/{movie['id']}")
                            if delete_response.status_code == 200:
                                st.success("Movie deleted successfully!")
                            else:
                                st.error(f"Failed to delete movie: {delete_response.text}")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                else:
                    st.error("Movie not found.")

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
            critics_rating = st.number_input("Critics Rating", min_value=0.0, max_value=10.0, step=0.1, key="critics_rating")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Movie"):
                    # Build the payload with critics_rating
                    movie_data = {
                        "title": movie_name,
                        "genre": genre,
                        "age_limit": age_restriction,
                        "director": director,
                        "duration_minutes": duration,
                        "release_date": str(release_date),
                        "critics_rating": critics_rating
                    }
                    response = requests.post(f"{BASE_URL}/movies", json=movie_data)
                    if response.status_code == 200:
                        st.success("Movie added successfully!")
                    else:
                        st.error(f"Failed to add movie: {response.text}")
    # Employees Section
    elif menu == "Employees":
        st.header("Employees Management")
        action = st.radio("Choose Action:", ["View Employees", "Add Employee"])

        if action == "View Employees":
            st.subheader("View Employee Details")
            try:
                # Fetch employee names for dropdown
                names_response = requests.get(f"{BASE_URL}/employees/dropdown")
                if names_response.status_code == 200:
                    employee_names = names_response.json()
                else:
                    st.error("Failed to fetch employee names.")
                    return

                # Select an employee by name
                selected_employee_name = st.selectbox("Select an Employee", employee_names)

                # Fetch all employee details
                details_response = requests.get(f"{BASE_URL}/employees")
                if details_response.status_code == 200:
                    employees = details_response.json()
                    # Find the selected employee by name
                    employee = next((e for e in employees if e["first_name"] + " " + e["last_name"] == selected_employee_name), None)
                else:
                    st.error("Failed to fetch employee details.")
                    return

                if employee:
                    # Display employee details
                    st.text_input("First Name", value=employee["first_name"], disabled=True)
                    st.text_input("Last Name", value=employee["last_name"], disabled=True)
                    st.text_input("Personal ID", value=employee["personal_id"], disabled=True)
                    st.text_input("Phone Number", value=employee["phone_number"], disabled=True)
                    st.text_input("Role", value=employee["role"], disabled=True)
                    st.text_input("City", value=employee["city"], disabled=True)
                    st.text_input("Salary", value=str(employee["salary"]), disabled=True)
                    st.text_input("Year of Birth", value=employee["birth_year"], disabled=True)
                    st.text_input("Year of Employment", value=employee["start_year"], disabled=True)
                    
                    if st.button("Delete Employee"):
                        try:
                            delete_response = requests.delete(f"{BASE_URL}/employees/{employee['id']}")
                            if delete_response.status_code == 200:
                                st.success("Employee deleted successfully!")
                            else:
                                st.error(f"Failed to delete employee: {delete_response.text}")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                else:
                    st.error("Employee not found.")

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
                    if not phone_number.isdigit():
                        st.error("Phone number must contain only digits.")
                    else:
                        employee_data = {
                            "personal_id": emp_id,
                            "phone_number": phone_number,
                            "first_name": first_name,
                            "last_name": last_name,
                            "birth_year": str(year_of_birth),
                            "start_year": str(year_of_employment),
                            "role": role,
                            "city": city_of_residence,
                            "salary": salary
                        }
                        response = requests.post(f"{BASE_URL}/employees", json=employee_data)
                        if response.status_code == 200:
                            st.success("Employee added successfully!")
                        else:
                            st.error(f"Failed to add employee: {response.text}")
    # Branches Section
    elif menu == "Branches": 
        st.header("Branches Management")
        action = st.radio("Choose Action:", ["View Branches", "Add Branch"])

        if action == "View Branches":
            st.subheader("View Branch Details")
            try:
                # Fetch branches from the backend
                response = requests.get(f"{BASE_URL}/branches")
                if response.status_code == 200:
                    branches = response.json()
                    branch_names = [branch["name"] for branch in branches]
                else:
                    st.error(f"Failed to fetch branches: {response.status_code}")
                    return

                # Select a branch
                selected_branch_name = st.selectbox("Select a Branch", branch_names)
                branch = next((b for b in branches if b["name"] == selected_branch_name), None)

                if branch:
                    # Display branch details
                    st.text_input("Branch Name", value=branch["name"], disabled=True)
                    st.text_input("Manager ID", value=branch["manager_id"], disabled=True)
                    st.text_input("Opening Time", value=branch["opening_time"], disabled=True)
                    st.text_input("Closing Time", value=branch["closing_time"], disabled=True)
                    st.text_input("Opening Year", value=branch["opening_year"], disabled=True)
                    st.text_input("Customer Service Phone", value=branch["customer_service_phone"], disabled=True)
                    
                    if st.button("Delete Branch"):
                        try:
                            delete_response = requests.delete(f"{BASE_URL}/branches/{branch['id']}")
                            if delete_response.status_code == 200:
                                st.success("Branch deleted successfully!")
                            else:
                                st.error(f"Failed to delete branch: {delete_response.text}")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                else:
                    st.error("Branch not found.")

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
                    if not customer_service_phone.isdigit():
                        st.error("Phone number must contain only digits.")
                    else:
                        branch_data = {
                            "name": branch_name,
                            "manager_id": manager_id,
                            "opening_time": str(opening_time),
                            "closing_time": str(closing_time),
                            "opening_year": str(opening_year),
                            "customer_service_phone": customer_service_phone
                        }
                        response = requests.post(f"{BASE_URL}/branches", json=branch_data)
                        if response.status_code == 200:
                            st.success("Branch added successfully!")
                        else:
                            st.error(f"Failed to add branch: {response.text}")
# Show the appropriate page
if not st.session_state.authenticated:
    login_page()
else:
    main_app()

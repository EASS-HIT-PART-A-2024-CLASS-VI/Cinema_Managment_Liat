import streamlit as st
import requests
import pandas as pd
import datetime

# API base URL
BASE_URL = "http://backend:8000"

def logout():
    """
    Logout function: Clears session state and redirects to login page.
    """
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.menu = "Employees"
    st.experimental_rerun()

def employees_page():
    """
    Render the Employees Management page.
    """
    st.markdown("""
        <style>
        .birthday-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
            transition: transform 0.2s ease-in-out;
            text-align: center;
        }
        .birthday-card:hover {
            transform: scale(1.05);
        }
        .birthday-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #FFD700;
        }
        .birthday-info {
            font-size: 1.2em;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)


    st.header("Employees Management")
    
    if st.session_state.get("show_birthdays", False):
        st.markdown("<h2 style='text-align: center; color: white;'>Employees with Birthdays this Month 🎂</h2>", unsafe_allow_html=True)
        try:
            response = requests.get(f"{BASE_URL}/employees/birthdays")
            if response.status_code == 200:
                birthday_employees = response.json()
                if not birthday_employees:
                    st.info("No employees have a birthday this month.")
                    return
                
                for emp in birthday_employees:
                    with st.expander(f" **{emp['first_name']} {emp['last_name']} ({emp['age']} years old)** 🎉"):
                        st.markdown(f"""
                            <div class="birthday-card">
                                <!-- FIX: Changed from emp['emp_id'] to emp['personal_id'] -->
                                <div class="birthday-info"><strong>ID:</strong> {emp['personal_id']}</div>
                                <div class="birthday-info"><strong>Role:</strong> {emp['role']}</div>
                                <div class="birthday-info"><strong>City:</strong> {emp['city']}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Failed to fetch birthday employees.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        return
    
    # הצגת רשימת עובדים ממיונים אם נלחץ הכפתור בסיידבאר
    if st.session_state.get("show_sorted_employees", False):
        st.subheader("Employees Sorted by Salary 💸")
        try:
            sorted_response = requests.get(f"{BASE_URL}/employees/sorted")
            if sorted_response.status_code == 200:
                sorted_employees = sorted_response.json()
                df = pd.DataFrame(sorted_employees, columns=["first_name", "last_name", "salary", "role"])
                df["Full Name"] = df["first_name"] + " " + df["last_name"]
                df = df[["Full Name", "salary", "role"]]
                df.columns = ["Full Name", "Salary", "Role"]
                st.dataframe(df, use_container_width=True)
            else:
                st.error("Failed to fetch sorted employees.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        # הצגת דף רגיל לניהול עובדים
        action = st.radio("Choose Action:", ["View Employees", "Add Employee"])

        if action == "View Employees":
            st.subheader("View Employee Details")

            try:
                names_response = requests.get(f"{BASE_URL}/employees/dropdown")
                if names_response.status_code == 200:
                    employee_names = names_response.json()
                else:
                    st.error("Failed to fetch employee names.")
                    return

                selected_employee_name = st.selectbox("Select an Employee", employee_names)

                details_response = requests.get(f"{BASE_URL}/employees")
                if details_response.status_code == 200:
                    employees = details_response.json()
                    employee = next(
                        (e for e in employees 
                         if e["first_name"] + " " + e["last_name"] == selected_employee_name), 
                        None
                    )
                else:
                    st.error("Failed to fetch employee details.")
                    return

                if employee:
                    st.text_input("First Name", value=employee["first_name"], disabled=True)
                    st.text_input("Last Name", value=employee["last_name"], disabled=True)
                    st.text_input("Personal ID", value=employee["personal_id"], disabled=True)
                    st.text_input("Phone Number", value=employee["phone_number"], disabled=True)
                    st.text_input("Role", value=employee["role"], disabled=True)
                    st.text_input("City", value=employee["city"], disabled=True)
                    st.text_input("Salary", value=str(employee["salary"]), disabled=True)
                    st.text_input("Year of Birth", value=employee["birth_year"], disabled=True)
                    st.text_input("Year of Employment", value=employee["start_year"], disabled=True)
                    
                    # כפתורי Delete ו-Logout בשורה אחת
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        if st.button("Delete Employee"):
                            try:
                                delete_response = requests.delete(f"{BASE_URL}/employees/{employee['id']}")
                                if delete_response.status_code == 200:
                                    st.success("Employee deleted successfully!")
                                else:
                                    st.error(f"Failed to delete employee: {delete_response.text}")
                            except Exception as e:
                                st.error(f"An error occurred: {e}")

                    with col2:
                        if st.button("Logout"):
                            logout()

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

            # כפתורי Save ו-Logout בשורה אחת
            col1, col2 = st.columns([1, 1])

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

            with col2:
                if st.button("Logout"):
                    logout()

import streamlit as st
import requests
import datetime
import pandas as pd

# API base URL
BASE_URL = "http://backend:8000"

def logout():
    """ Logout function: Clears session state and redirects to login page. """
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.menu = "Branches"
    st.rerun()  # מבצע רענון מידי ומחזיר לדף הלוגין

def branches_page():
    """
    Render the Branches Management page.
    """
    st.header("Branches Management")
    action = st.radio("Choose Action:", ["View Branches", "Add Branch"])

    if action == "View Branches":
        st.subheader("View Branch Details")
        try:
            response = requests.get(f"{BASE_URL}/branches")
            if response.status_code == 200:
                branches = response.json()
                branch_names = [branch["name"] for branch in branches]
            else:
                st.error(f"Failed to fetch branches: {response.status_code}")
                return

            selected_branch_name = st.selectbox("Select a Branch", branch_names)
            branch = next((b for b in branches if b["name"] == selected_branch_name), None)

            if branch:
                st.text_input("Branch Name", value=branch["name"], disabled=True)
                st.text_input("Manager ID", value=branch["manager_id"], disabled=True)
                st.text_input("Opening Time", value=branch["opening_time"], disabled=True)
                st.text_input("Closing Time", value=branch["closing_time"], disabled=True)
                st.text_input("Opening Year", value=branch["opening_year"], disabled=True)
                st.text_input("Customer Service Phone", value=branch["customer_service_phone"], disabled=True)
                
                # 🔹 כפתורי Delete ו-Logout בשורה אחת
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button("Delete Branch"):
                        try:
                            delete_response = requests.delete(f"{BASE_URL}/branches/{branch['id']}")
                            if delete_response.status_code == 200:
                                st.success("Branch deleted successfully!")
                            else:
                                st.error(f"Failed to delete branch: {delete_response.text}")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                with col2:
                    if st.button("Logout"):
                        logout()

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

        # 🔹 כפתורי Save ו-Logout בשורה אחת
        col1, col2 = st.columns([1, 1])

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

        with col2:
            if st.button("Logout"):
                logout()

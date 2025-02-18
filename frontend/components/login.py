import streamlit as st
import requests
from components.utils import set_background

BASE_URL = "http://backend:8000"

def login_page():
    """
    Render the login page with its specific background and login functionality.
    """
    set_background("/app/assets/background.png")

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
                    st.rerun()  
                elif response.status_code == 401:
                    st.error("Invalid username or password.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

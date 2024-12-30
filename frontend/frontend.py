import streamlit as st
import requests

API_URL = "http://localhost:8000"

def fetch_data(endpoint):
    response = requests.get(f"{API_URL}/{endpoint}")
    return response.json()

st.title('Movie Theater Management')

# Display branches
branches = fetch_data("branches")
if st.button('Show Branches'):
    st.write(branches)

# Display employees
employees = fetch_data("employees")
if st.button('Show Employees'):
    st.write(employees)

# Display movies
movies = fetch_data("movies")
if st.button('Show Movies'):
    st.write(movies)

# Form to add a branch
with st.form(key='branch_form'):
    name = st.text_input('Branch Name')
    manager_id = st.text_input('Manager ID')
    opening_time = st.text_input('Opening Time')
    closing_time = st.text_input('Closing Time')
    opening_year = st.number_input('Opening Year')
    customer_service_phone = st.text_input('Customer Service Phone')
    
    submit_button = st.form_submit_button(label='Add Branch')
    
    if submit_button:
        data = {
            "name": name,
            "manager_id": manager_id,
            "opening_time": opening_time,
            "closing_time": closing_time,
            "opening_year": opening_year,
            "customer_service_phone": customer_service_phone
        }
        response = requests.post(f"{API_URL}/branches", json=data)
        st.write(response.json())

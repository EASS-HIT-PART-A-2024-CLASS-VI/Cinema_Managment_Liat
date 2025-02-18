import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://backend:8000"

def logout():
    """
    Logout function: Clears session state and redirects to login page.
    """
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.menu = "Movies"
    st.experimental_rerun()

def sidebar():
    """
    Render the sidebar only if the user is authenticated.
    """
    if not st.session_state.authenticated:
        return  # לא מציג תפריט אם המשתמש לא מחובר

    st.sidebar.title(f"Welcome, {st.session_state.username}")

    # תפריט ניווט
    menu_options = ["Movies", "Employees", "Branches"]
    st.session_state.menu = st.sidebar.selectbox("Menu", menu_options)

    # כפתור להצגת סרטים מדורגים
    if st.session_state.menu == "Movies":
        if st.sidebar.button("Show Sorted Movies 🎬"):
            st.session_state.show_sorted_movies = True
        else:
            st.session_state.show_sorted_movies = False

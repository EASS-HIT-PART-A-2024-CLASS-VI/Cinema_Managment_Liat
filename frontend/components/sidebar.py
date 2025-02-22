import streamlit as st
import requests

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
    
    # Get previous menu selection
    previous_menu = st.session_state.get("menu")
    
    # Update menu selection
    current_menu = st.sidebar.selectbox("Menu", menu_options)
    st.session_state.menu = current_menu
    
    # Reset manage_screenings when switching away from Branches
    if previous_menu == "Branches" and current_menu != "Branches":
        st.session_state.manage_screenings = False

    # כפתור "Show Sorted Movies" מופיע רק אם נמצאים בעמוד Movies
    if st.session_state.menu == "Movies":
        if st.sidebar.button("Show Sorted Movies 🎬"):
            st.session_state.show_sorted_movies = True
        else:
            st.session_state.show_sorted_movies = False

    # כפתורים ייעודיים לעמוד Employees
    if st.session_state.menu == "Employees":
        if st.sidebar.button("Sort Employees by Salary 💰"):
            st.session_state.show_sorted_employees = True
        else:
            st.session_state.show_sorted_employees = False

        if st.sidebar.button("Birthdays 🎂"):
            st.session_state.show_birthdays = True
        else:
            st.session_state.show_birthdays = False

    # כפתור לניהול לוח ההקרנות יופיע **רק** אם נמצאים בעמוד Branches
    if st.session_state.menu == "Branches":
        # אם לוחצים עליו, נגדיר manage_screenings = True;
        # אם לא לוחצים — לא נדרוס את הערך, כדי לא למחוק מצב קודם.
        if st.sidebar.button("Manage Screenings 📽️"):
            st.session_state.manage_screenings = True
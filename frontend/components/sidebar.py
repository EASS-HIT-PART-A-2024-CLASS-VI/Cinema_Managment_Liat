import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://backend:8000"

def sidebar():
    """
    Render the sidebar only if the user is authenticated.
    """
    if not st.session_state.authenticated:
        return  #  לא מציג תפריט אם המשתמש לא מחובר

    st.sidebar.title(f"Welcome, {st.session_state.username}")

    # תפריט ניווט - מסיר את "app" ושומר רק על Movies, Employees, Branches
    menu_options = ["Movies", "Employees", "Branches"]
    st.session_state.menu = st.sidebar.selectbox("Menu", menu_options)

    #  הכפתור יוצג **רק אם התפריט על Movies**
    if st.session_state.menu == "Movies":
        if st.sidebar.button("Show Sorted Movies 🎬"):
            st.session_state.show_sorted_movies = True  # סימון שהכפתור נלחץ
        else:
            st.session_state.show_sorted_movies = False  # איפוס כאשר לא לוחצים

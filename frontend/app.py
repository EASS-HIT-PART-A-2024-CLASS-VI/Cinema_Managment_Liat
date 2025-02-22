import streamlit as st
import requests
from components.login import login_page
from components.sidebar import sidebar
from pages.movies import movies_page
from pages.employees import employees_page
from pages.branches import branches_page
from components.utils import set_background

# Base URL for API requests
BASE_URL = "http://backend:8000"

# 📌 הגדרת פריסת העמוד
st.set_page_config(page_title="Cinema Management System", page_icon="🍿", initial_sidebar_state="collapsed")

# 🔹 הסתרת הניווט האוטומטי של Streamlit
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

def initialize_session():
    """Ensure necessary session state variables are initialized."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "menu" not in st.session_state:
        st.session_state.menu = "Movies"
    if "show_chatbot" not in st.session_state:
        st.session_state.show_chatbot = False
    if "show_sorted_movies" not in st.session_state:
        st.session_state.show_sorted_movies = False
    if "show_sorted_employees" not in st.session_state:
        st.session_state.show_sorted_employees = False
    if "show_birthdays" not in st.session_state:
        st.session_state.show_birthdays = False
    if "manage_screenings" not in st.session_state:
        st.session_state.manage_screenings = False

def chatbot_ui():
    """Displays the chatbot interface."""
    st.subheader("Cinema Chatbot 🤖")
    user_query = st.text_input("Your Question:", key="chat_input")
    
    if st.button("Send", key="send_chat"):
        if user_query.strip():
            response = requests.post(
                f"{BASE_URL}/api/llm/chat", 
                json={"prompt": user_query}
            )
            if response.status_code == 200:
                st.write("**Bot:** " + response.json().get("response", "No response received."))
            else:
                st.error("Error communicating with chatbot.")

def main():
    initialize_session()

    if not st.session_state.authenticated:
        login_page()
        return

    # Update states based on sidebar interactions
    sidebar()
    menu = st.session_state.menu

    # Show either chatbot OR regular content, not both
    if st.session_state.show_chatbot:
        set_background("/app/assets/moviesback.png")  # You can choose which background to use
        chatbot_ui()
    else:
        # Display regular page content
        if menu == "Movies":
            set_background("/app/assets/moviesback.png")
            movies_page()
        elif menu == "Employees":
            set_background("/app/assets/employeeback.png")
            employees_page()
        elif menu == "Branches":
            set_background("/app/assets/branchesback.png")
            branches_page()

if __name__ == "__main__":
    main()
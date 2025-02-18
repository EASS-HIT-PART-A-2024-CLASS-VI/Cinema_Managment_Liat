import streamlit as st
from components.login import login_page
from components.sidebar import sidebar
from pages.movies import movies_page
from pages.employees import employees_page
from pages.branches import branches_page
from components.utils import set_background

# 📌 הגדרת פריסת העמוד תוך ביטול תפריט הניווט האוטומטי אבל שמירת "Settings" ו-"Deploy"
st.set_page_config(page_title="Cinema Management System", page_icon="🍿", initial_sidebar_state="collapsed")

# 🔹 הסתרת התפריט האוטומטי של Streamlit בלבד, אך השארת ה-Settings & Deploy
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;} /* מסתיר את הניווט האוטומטי של Streamlit */
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

def main():
    initialize_session()

    # 📌 הצגת דף הלוגין ללא ה-sidebar
    if not st.session_state.authenticated:
        login_page()
        return  # מונע טעינת המערכת אם המשתמש לא מחובר

    # ✅ מציג את ה-sidebar **רק אם המשתמש מחובר**
    sidebar()
    menu = st.session_state.menu

    # ✅ מציג את הדף הנבחר בלבד
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

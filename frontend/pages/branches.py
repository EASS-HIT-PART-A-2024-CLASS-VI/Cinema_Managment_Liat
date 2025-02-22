import streamlit as st
import requests
import datetime
import math

# API base URL
BASE_URL = "http://backend:8000"

# הימים שיוצגו בטבלת ההקרנות
DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def logout():
    """
    Logout function: Clears session state and redirects to login page.
    """
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.menu = "Branches"
    try:
        st.rerun()  # אם אינו קיים בגרסתך, החלף ב-st.stop() או הסר לחלוטין.
    except:
        st.stop()


def delete_movie_from_schedule(movie_title):
    """
    אם סרט נמחק מה-DB, יש להסירו מכל הלוחות (לו"ז) שב-session_state.
    פונקציה זו עוברת על כל חבילת ה-screenings בסשן ומוחקת את הסרט אם הוא משובץ.
    שים לב שיש לקרוא לה לאחר מחיקה מוצלחת מה-DB (באותו מקום בקוד שבו מוחקים).
    """
    for key in list(st.session_state.keys()):
        if key.startswith("screenings_"):
            for hall in st.session_state[key]:
                for day in st.session_state[key][hall]:
                    for time_slot in list(st.session_state[key][hall][day].keys()):
                        if st.session_state[key][hall][day][time_slot] == movie_title:
                            st.session_state[key][hall][day][time_slot] = None


def branches_page():
    """
    עמוד Branches רגיל. אם manage_screenings=True, מציגים את לוח ההקרנות במקום.
    """
    if st.session_state.get("manage_screenings", False):
        manage_screenings_page()
        return

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


def manage_screenings_page():
    """
    Manages movie screenings for different branches
    """
    st.header("Manage Screenings")

    try:
        response = requests.get(f"{BASE_URL}/branches")
        if response.status_code == 200:
            branches = response.json()
            branch_names = [branch["name"] for branch in branches]
        else:
            st.error(f"Failed to fetch branches: {response.status_code}")
            return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return

    selected_branch_name = st.selectbox("Select a Branch", ["---"] + branch_names)
    if selected_branch_name == "---":
        st.info("Please select a branch to manage its schedule.")
        if st.button("Back to Branches"):
            st.session_state["manage_screenings"] = False
            try:
                st.rerun()
            except:
                st.stop()
        return

    branch = next((b for b in branches if b["name"] == selected_branch_name), None)
    if not branch:
        st.error("Branch not found.")
        return

    st.markdown(f"**Selected Branch:** {selected_branch_name} (ID: {branch['id']})")
    manage_screenings(branch)

def manage_screenings(branch_info):
    branch_id = branch_info["id"]

    # Fetch current movies from DB
    response = requests.get(f"{BASE_URL}/movies")
    if response.status_code == 200:
        movies = response.json()
        movie_durations = {m["title"]: m["duration_minutes"] for m in movies}
        available_titles = list(movie_durations.keys())
    else:
        st.error("Failed to fetch movies.")
        return

    try:
        open_dt = datetime.datetime.strptime(branch_info["opening_time"], "%H:%M:%S").time()
        close_dt = datetime.datetime.strptime(branch_info["closing_time"], "%H:%M:%S").time()
    except ValueError:
        open_dt = datetime.datetime.strptime(str(branch_info["opening_time"]), "%H:%M").time()
        close_dt = datetime.datetime.strptime(str(branch_info["closing_time"]), "%H:%M").time()

    open_hour = open_dt.hour
    close_hour = close_dt.hour

    if close_hour == 0:
        close_hour = 24

    if close_hour < open_hour:
        hours_list = list(range(open_hour, 24)) + list(range(0, close_hour))
    else:
        hours_list = list(range(open_hour, close_hour))

    session_key = f"screenings_{branch_id}"
    if session_key not in st.session_state:
        st.session_state[session_key] = {
            hall: {
                day: {f"{hour}:00": None for hour in hours_list}
                for day in DAYS_OF_WEEK
            }
            for hall in range(1, 4)
        }

    # Clean up deleted movies from schedule
    for hall in range(1, 4):
        for day in DAYS_OF_WEEK:
            for hour_str in st.session_state[session_key][hall][day].keys():
                current_movie = st.session_state[session_key][hall][day][hour_str]
                if current_movie and current_movie not in movie_durations:
                    st.session_state[session_key][hall][day][hour_str] = None
                    st.warning(f"Removed '{current_movie}' from schedule as it no longer exists in database.")

    st.subheader("Available Movies")
    st.write("Select a movie you want to schedule, then click on a free timeslot below.")

    selected_movie = st.selectbox("Pick a movie to schedule", ["- None -"] + available_titles)
    if selected_movie == "- None -":
        selected_movie = None

    st.markdown("---")

    def schedule_movie(hall, day, start_hour_str, movie_title):
        if not movie_title:
            st.warning("No movie selected!")
            return
        if movie_title not in movie_durations:
            st.warning("Selected movie is no longer available.")
            return

        dur_hours = math.ceil(movie_durations[movie_title] / 60.0)
        start_h = int(start_hour_str.split(":")[0])
        end_h = start_h + dur_hours

        for h in range(start_h, end_h):
            if h not in hours_list:
                st.warning(f"Cannot schedule '{movie_title}' at {start_hour_str} - outside branch operating hours.")
                return

        for h in range(start_h, end_h):
            slot_str = f"{h}:00"
            if st.session_state[session_key][hall][day][slot_str] is not None:
                st.warning(f"Cannot schedule '{movie_title}' - conflict in Hall {hall}, {day} at {slot_str}.")
                return

        for h in range(start_h, end_h):
            slot_str = f"{h}:00"
            st.session_state[session_key][hall][day][slot_str] = movie_title

        st.success(f"Scheduled '{movie_title}' on {day}, {start_hour_str} (Hall {hall}).")

    def remove_movie(hall, day, start_hour_str, current_movie):
        if current_movie not in movie_durations:
            mov_dur = 1  # Default to 1 hour if movie duration unknown
        else:
            mov_dur = math.ceil(movie_durations[current_movie] / 60.0)
        
        start_h = int(start_hour_str.split(":")[0])
        
        for h in range(start_h, start_h + mov_dur):
            slot_str = f"{h}:00"
            if slot_str in st.session_state[session_key][hall][day]:
                if st.session_state[session_key][hall][day][slot_str] == current_movie:
                    st.session_state[session_key][hall][day][slot_str] = None
        
        st.success(f"Removed '{current_movie}' from {day}, {start_hour_str} (Hall {hall}).")
        st.session_state["schedule_updated"] = True

    for hall in range(1, 4):
        st.markdown(f"## Hall {hall}")
        for day in DAYS_OF_WEEK:
            st.markdown(f"### {day}")
            timeslots = st.session_state[session_key][hall][day]

            for hour_str, current_movie in timeslots.items():
                with st.container():
                    col1, col2 = st.columns([1, 3])  # Align time and button side by side
                    with col1:
                        st.markdown(f"""
                                     <div style='padding: 10px; background: rgba(0,0,0,0.5); border-radius: 10px;'>
                                     <strong>{hour_str}</strong> - {'**' + current_movie + '**' if current_movie else '*Free*'}
                                     </div>
                                    """, unsafe_allow_html=True)
                    with col2:
                        button_style = """
                        <style>
                        div.stButton > button {
                            width: 100%;
                            background-color: rgba(0,0,0,0.7);
                            color: white;
                            border-radius: 8px;
                            padding: 10px;
                            border: none;
                            transition: 0.3s;
                        }
                        div.stButton > button:hover {
                            background-color: rgba(255, 215, 0, 0.8);
                            color: black;
                        }
                        </style>
                        """
                        st.markdown(button_style, unsafe_allow_html=True)
                        
                        if current_movie:
                            if st.button(f"Remove {current_movie} at {hour_str} Hall {hall}", 
                                         key=f"remove_{hall}_{day}_{hour_str}"):
                                remove_movie(hall, day, hour_str, current_movie)
                        else:
                            if st.button(f"Schedule {day} {hour_str} Hall {hall}", 
                                         key=f"schedule_{hall}_{day}_{hour_str}"):
                                schedule_movie(hall, day, hour_str, selected_movie)

    st.markdown("---")

    if st.button("Back to Branches"):
        st.session_state["manage_screenings"] = False
        try:
            st.rerun()
        except:
            st.stop()

    if "schedule_updated" in st.session_state and st.session_state["schedule_updated"]:
        st.session_state["schedule_updated"] = False
        st.rerun()
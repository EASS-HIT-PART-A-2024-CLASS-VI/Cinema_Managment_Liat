import streamlit as st
import requests
import pandas as pd
import datetime

BASE_URL = "http://backend:8000"

def logout():
    """ Logout function: Clears session state and redirects to login page. """
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.menu = "Movies"
    st.rerun()  # מבצע רענון ומחזיר לדף הלוגין

def delete_movie_from_schedule(movie_title):
    """
    Remove a deleted movie from all schedules in session state.
    """
    for key in st.session_state.keys():
        if key.startswith("screenings_"):  # מחפשים את לוחות ההקרנות של כל הסניפים
            for hall in st.session_state[key]:
                for time in st.session_state[key][hall]:
                    if st.session_state[key][hall][time] == movie_title:
                        st.session_state[key][hall][time] = None  # פינוי המקום בלוז
def movies_page():
    """
    Render the Movies Management page.
    """
    st.header("Movies Management")

    # בדיקה אם המשתמש לחץ על "Show Sorted Movies" - אם כן, מציג רק את הטבלה
    if st.session_state.get("show_sorted_movies", False):
        st.subheader("Sorted Movies by Rating 🎬")

        response = requests.get(f"{BASE_URL}/movies/sorted")
        if response.status_code == 200:
            movies = response.json()
            if movies:
                df = pd.DataFrame(movies)
                df = df[["title", "critics_rating", "genre"]]
                df.columns = ["Movie Name", "Rating", "Genre"]
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No movies found in the database.")
        else:
            st.error("Failed to fetch movies from the API.")
        
        return  # מסיים כאן, כדי שלא יוצג דף ניהול הסרטים

    # אם הכפתור לא נלחץ - מציג את ממשק ניהול הסרטים הרגיל
    action = st.radio("Choose Action:", ["View Movies", "Add Movie"], key="movie_action")

    if action == "View Movies":
        st.subheader("View Movie Details")
        try:
            # Fetch movie titles for dropdown
            titles_response = requests.get(f"{BASE_URL}/movies/dropdown")
            if titles_response.status_code == 200:
                movie_titles = titles_response.json()
            else:
                st.error("Failed to fetch movie titles.")
                return

            # Select a movie title
            selected_title = st.selectbox("Select a Movie", movie_titles, key="selected_movie")

            # Fetch all movie details
            details_response = requests.get(f"{BASE_URL}/movies")
            if details_response.status_code == 200:
                movies = details_response.json()
                movie = next((m for m in movies if m["title"] == selected_title), None)
            else:
                st.error("Failed to fetch movie details.")
                return

            if movie:
                st.text_input("Title", value=movie["title"], disabled=True)
                st.text_input("Genre", value=movie["genre"], disabled=True)
                st.text_input("Director", value=movie["director"], disabled=True)
                st.text_input("Age Restriction", value=str(movie["age_limit"]), disabled=True)
                st.text_input("Duration (minutes)", value=str(movie["duration_minutes"]), disabled=True)
                st.text_input("Release Date", value=movie["release_date"], disabled=True)
                st.text_input("Critics Rating", value=str(movie["critics_rating"]), disabled=True)

                # כפתורי Delete ו-Logout בשורה אחת
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button("Delete Movie"):
                        try:
                            delete_response = requests.delete(f"{BASE_URL}/movies/{movie['id']}")
                            if delete_response.status_code == 200:
                                st.success("Movie deleted successfully!")
                            else:
                                st.error(f"Failed to delete movie: {delete_response.text}")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                with col2:
                    if st.button("Logout"):
                        logout()
            else:
                st.error("Movie not found.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    elif action == "Add Movie":
        st.subheader("Add a New Movie")
        movie_name = st.text_input("Movie Name", key="movie_name")
        genre = st.selectbox(
            "Genre",
            ["Comedy", "Romance", "Action", "Horror", "Sci-Fi", "Fantasy", "Thriller", "Drama", "Mystery", "Documentary"],
            key="genre"
        )
        age_restriction = st.selectbox("Age Restriction", [True, False], key="age_restriction")
        director = st.text_input("Director Name", key="director")
        duration = st.number_input("Duration (minutes)", min_value=1, step=1, key="duration")
        release_date = st.date_input("Release Date", min_value=datetime.date(1970, 1, 1), key="release_date")
        critics_rating = st.number_input("Critics Rating", min_value=0.0, max_value=10.0, step=0.1, key="critics_rating")

        # כפתורי Save ו-Logout בשורה אחת
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Save Movie"):
                movie_data = {
                    "title": movie_name,
                    "genre": genre,
                    "age_limit": age_restriction,
                    "director": director,
                    "duration_minutes": duration,
                    "release_date": str(release_date),
                    "critics_rating": critics_rating
                }
                response = requests.post(f"{BASE_URL}/movies", json=movie_data)
                if response.status_code == 200:
                    st.success("Movie added successfully!")
                else:
                    st.error(f"Failed to add movie: {response.text}")

        with col2:
            if st.button("Logout"):
                logout()

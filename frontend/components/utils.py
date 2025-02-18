import streamlit as st
import base64

@st.cache_data
def get_encoded_background(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def set_background(image_path):
    """
    Apply a full-page background image dynamically to cover the entire page,
    including the sidebar and header. All text remains styled as white.
    """
    try:
        encoded_string = get_encoded_background(image_path)
        st.markdown(
            f"""
            <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: white !important;
            }}
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .block-container {{
                padding: 2rem;
                color: white !important;
            }}
            header {{
                background: transparent !important;
                color: white !important;
            }}
            .stSidebar {{
                background-color: black !important;
                color: white !important;
            }}
            .stSidebar .css-1d391kg {{
                color: white !important;
            }}
            label {{
                color: white !important;
                font-size: 18px;
            }}
            .stButton>button {{
                background-color: black !important;
                color: white !important;
                font-weight: bold;
                border-radius: 5px;
                border: none;
                padding: 10px 20px;
            }}
            input, select, textarea {{
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid white !important;
                font-size: 16px;
            }}
            input[disabled], select[disabled], textarea[disabled] {{
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid white !important;
                opacity: 1 !important; /* Fix opacity issues for disabled fields */
            }}
            .stRadio > div {{
                color: white !important; /* Ensure radio buttons are styled */
            }}
            .stRadio > div > label {{
                color: white !important;
                font-size: 16px;
                font-weight: bold;
            }}
            [data-baseweb="select"] > div, [data-testid="stTimeInput"] > div {{
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid white !important;
                font-size: 16px;
                border-radius: 5px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("Background image not found. Please check the file path.")

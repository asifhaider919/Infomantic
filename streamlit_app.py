import streamlit as st

# Define correct username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "admin"

# Title of the app
st.title("Login Page")

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Function to handle login
def login():
    if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
        st.session_state['logged_in'] = True
        st.success("Login successful!")
    else:
        st.error("Incorrect username or password. Please try again.")

# If the user is not logged in, display the login form
if not st.session_state['logged_in']:
    # Add login components
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Add login button
    if st.button("Login"):
        login()
else:
    # If logged in, display welcome message
    st.title("Welcome!")

import streamlit as st
import pandas as pd
import os

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
    # If logged in, display welcome message and file upload option
    st.title("Welcome!")
    st.write("Please upload an XLS, XLSX, or CSV file.")
    
    uploaded_file = st.file_uploader("Choose a file", type=["xls", "xlsx", "csv"])
    
    if uploaded_file is not None:
        # Determine the file extension
        file_extension = os.path.splitext(uploaded_file.name)[1]
        
        # Save the uploaded file with the correct extension
        file_path = f"Input_Data{file_extension}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File saved as {file_path}")

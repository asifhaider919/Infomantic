import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
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

        # Read the uploaded file into a pandas DataFrame
        try:
            if file_extension in ['.xls', '.xlsx']:
                data = pd.read_excel(uploaded_file)
            else:
                data = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
            st.stop()
        
        # Ensure the required columns are present
        if 'Site' not in data.columns or 'Lat' not in data.columns or 'Lon' not in data.columns:
            st.error("The uploaded file must contain 'Site', 'Lat', and 'Lon' columns.")
        else:
            # Create a Folium map centered around the mean location of all data
            m = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=5)

            # Display markers for all data
            for idx, row in data.iterrows():
                # Create a popup message with site information and issue details
                popup_message = f"<b>Site Name:</b> {row['Site']}<br>" \
                                f"<b>Latitude:</b> {row['Lat']}<br>" \
                                f"<b>Longitude:</b> {row['Lon']}<br>"

                # Add additional columns to the popup message if present
                additional_columns = row.index.difference(['Site', 'Lat', 'Lon'])
                for col in additional_columns:
                    popup_message += f"<b>{col}:</b> {row[col]}<br>"

                folium.Marker(
                    location=[row['Lat'], row['Lon']],
                    popup=folium.Popup(popup_message, max_width=400),  # Increase max_width as needed
                    icon=folium.Icon(color='blue', icon='cloud')
                ).add_to(m)

            # Display the map in the Streamlit app
            st_folium(m, width=900, height=700)

            # Allow user to filter by site name to navigate map
            search_site_name = st.text_input("Enter Site Name to Filter and Navigate Map:")
            if search_site_name:
                filtered_data = data[data['Site'].str.contains(search_site_name, case=False)]
                if not filtered_data.empty:
                    # Display filtered data in a table
                    st.subheader(f"Filtered Data for Site Name containing '{search_site_name}'")
                    st.write(filtered_data)

                    # Zoom in on the map to the first filtered location
                    folium_map = folium.Map(location=[filtered_data['Lat'].mean(), filtered_data['Lon'].mean()], zoom_start=10)
                    for idx, row in filtered_data.iterrows():
                        popup_message = f"<b>Site Name:</b> {row['Site']}<br>" \
                                        f"<b>Latitude:</b> {row['Lat']}<br>" \
                                        f"<b>Longitude:</b> {row['Lon']}<br>"

                        additional_columns = row.index.difference(['Site', 'Lat', 'Lon'])
                        for col in additional_columns:
                            popup_message += f"<b>{col}:</b> {row[col]}<br>"

                        folium.Marker(
                            location=[row['Lat'], row['Lon']],
                            popup=folium.Popup(popup_message, max_width=400),
                            icon=folium.Icon(color='blue', icon='cloud')
                        ).add_to(folium_map)

                    st_folium(folium_map, width=900, height=700)
                else:
                    st.warning(f"No data found for Site Name containing '{search_site_name}'.")
    else:
        st.info("Please upload a file")

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Define correct username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "admin"

# Title of the app
st.title("Login to Access Site Map")

# Add login components
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Check if username and password are correct
if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
    st.success("Login successful!")

    # Upload CSV file for site data
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            # Try to read the CSV file with UTF-8 encoding
            data = pd.read_csv(uploaded_file, encoding='utf-8')
            print("Columns in CSV file:", data.columns.tolist())  # Debugging: Print column names
        except UnicodeDecodeError:
            # If there's a UnicodeDecodeError, try reading with ISO-8859-1 encoding
            data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        else:
            # Check if the dataframe is empty
            if data.empty:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
            else:
                # Display the data
                st.write("Data preview:")
                st.write(data)

                # Check if the required columns are in the dataframe
                required_columns = ['SiteName', 'Latitude', 'Longitude', 'Issue']
                if all(col in data.columns for col in required_columns):
                    # Create a Folium map centered around the mean location
                    m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=5)

                    # Extract distinct issues and assign unique colors
                    distinct_issues = data['Issue'].unique()
                    issue_color_map = {issue: folium.utilities.get_random_color() for issue in distinct_issues}

                    for idx, row in data.iterrows():
                        # Determine color based on issue category
                        issue_color = issue_color_map.get(row['Issue'], 'blue')

                        # Create a popup message with site information and issue details
                        popup_message = f"<b>Site Name:</b> {row['SiteName']}<br>" \
                                        f"<b>Latitude:</b> {row['Latitude']}<br>" \
                                        f"<b>Longitude:</b> {row['Longitude']}<br>" \
                                        f"<b>Issue:</b> {row['Issue']}<br>"

                        folium.CircleMarker(
                            location=[row['Latitude'], row['Longitude']],
                            radius=10,
                            popup=folium.Popup(popup_message, max_width=300),
                            color=issue_color,
                            fill=True,
                            fill_color=issue_color
                        ).add_to(m)

                    # Display the map in the Streamlit app
                    st_folium(m, width=700, height=500)
                else:
                    st.error("CSV file must contain 'SiteName', 'Latitude', 'Longitude', and 'Issue' columns")
    else:
        st.info("Please upload a CSV file")
else:
    if username != "" or password != "":
        st.error("Incorrect username or password. Please try again.")

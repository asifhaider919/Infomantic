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
                if 'SiteName' in data.columns and 'Latitude' in data.columns and 'Longitude' in data.columns:
                    # Create a Folium map centered around the mean location
                    m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=5)

                    # Add circle markers to the map with color based on a new column (if it exists)
                    if 'Color' in data.columns:
                        color_column = 'Color'
                    else:
                        color_column = None

                    for idx, row in data.iterrows():
                        color = row[color_column] if color_column else 'blue'
                        # Create a popup message with additional information
                        popup_message = f"<b>Site Name:</b> {row['SiteName']}<br>" \
                                        f"<b>Latitude:</b> {row['Latitude']}<br>" \
                                        f"<b>Longitude:</b> {row['Longitude']}<br>"
                        if 'Info' in data.columns:
                            popup_message += f"<b>Info:</b> {row['Info']}<br>"

                        folium.CircleMarker(
                            location=[row['Latitude'], row['Longitude']],
                            radius=10,
                            popup=folium.Popup(popup_message, max_width=300),
                            color=color,
                            fill=True,
                            fill_color=color
                        ).add_to(m)

                    # Display the map in the Streamlit app
                    st_folium(m, width=700, height=500)
                else:
                    st.error("CSV file must contain 'SiteName', 'Latitude', and 'Longitude' columns")
    else:
        st.info("Please upload a CSV file")
else:
    if username != "" or password != "":
        st.error("Incorrect username or password. Please try again.")

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Title of the app
st.title("Site Map")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Display the data
    st.write("Data preview:")
    st.write(data)

    # Check if the required columns are in the dataframe
    if 'SiteName' in data.columns and 'Latitude' in data.columns and 'Longitude' in data.columns:
        # Create a Folium map centered around the mean location
        m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=5)

        # Add circle markers to the map
        for idx, row in data.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=10,
                popup=row['SiteName'],
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)

        # Display the map in the Streamlit app
        st_folium(m, width=700, height=500)
    else:
        st.error("CSV file must contain 'SiteName', 'Latitude', and 'Longitude' columns")
else:
    st.info("Please upload a CSV file")

import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Google Map in Streamlit")

# Define the initial location and zoom level
initial_lat = 37.7749  # Latitude for San Francisco
initial_lon = -122.4194  # Longitude for San Francisco
initial_zoom = 12

# Create a Folium map
m = folium.Map(location=[initial_lat, initial_lon], zoom_start=initial_zoom)

# Add a marker for the initial location
folium.Marker(
    location=[initial_lat, initial_lon],
    popup="San Francisco",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

# Display the map in the Streamlit app
st_folium(m, width=700, height=500)

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Set page configuration
st.set_page_config(layout="wide")

# Title of the app
st.title("Draw Lines from Site A to Site B")

# Sidebar for file upload
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read the uploaded file into a pandas DataFrame
        data = pd.read_excel(uploaded_file)
        
        # Check for required columns
        required_columns = ['Site_A', 'Site_B', 'Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']
        if all(col in data.columns for col in required_columns):
            # Convert relevant columns to numeric (in case they are not already)
            numeric_columns = ['Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']
            data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
            
            # Create a map centered around the mean location of the data
            m = folium.Map(location=[data[['Lat_A', 'Lat_B']].mean().mean(), 
                                      data[['Lon_A', 'Lon_B']].mean().mean()], zoom_start=7)
            
            # Iterate through rows to draw lines
            for index, row in data.iterrows():
                # Skip rows with missing or NaN values
                if row.isnull().any():
                    continue
                
                # Add a line from Lat_A/Lon_A to Lat_B/Lon_B
                folium.PolyLine(locations=[(row['Lat_A'], row['Lon_A']), (row['Lat_B'], row['Lon_B'])],
                                color='blue').add_to(m)
            
            # Display the map
            folium_static(m)
            
        else:
            st.sidebar.warning(f"Required columns {required_columns} not found in the file.")
    
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

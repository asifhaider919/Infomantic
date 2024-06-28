import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Title of the app
st.title("Upload File to Plot Sites on Map")

# Upload CSV file for site data
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    # Save the uploaded file
    with open(f"Input_Data.{uploaded_file.name.split('.')[-1]}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File saved as Input_Data.{uploaded_file.name.split('.')[-1]}")
    
    try:
        # Read the uploaded file into a pandas DataFrame
        if uploaded_file.name.endswith('.xls') or uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
        
        # Ensure the required columns are present
        if 'Lat' not in data.columns or 'Lon' not in data.columns or 'Site' not in data.columns:
            st.error("The uploaded file must contain 'Site', 'Lat', and 'Lon' columns.")
        else:
            # Sidebar filter by Site Name
            st.sidebar.subheader("Filter by Site Name")
            search_site_name = st.sidebar.text_input("Enter Site Name")
            
            # Create initial map centered around the mean location of all data
            m = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=3)

            # Display markers for filtered data or all data if not filtered
            if search_site_name:
                filtered_data = data[data['Site'].str.contains(search_site_name, case=False)]
                if not filtered_data.empty:
                    # Calculate bounds to zoom to 10km around the first filtered site
                    first_site = filtered_data.iloc[0]
                    bounds = [(first_site['Lat'] - 0.05, first_site['Lon'] - 0.05), 
                              (first_site['Lat'] + 0.05, first_site['Lon'] + 0.05)]
                    
                    for idx, row in filtered_data.iterrows():
                        # Create a popup message with site information
                        popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                        f"<b>Latitude:</b> {row['Lat']}<br>" \
                                        f"<b>Longitude:</b> {row['Lon']}<br>"

                        folium.Marker(
                            location=[row['Lat'], row['Lon']],
                            popup=folium.Popup(popup_message, max_width=400),
                            icon=folium.Icon(color='blue', icon='cloud')
                        ).add_to(m)
                    
                    # Fit the map to the bounds
                    m.fit_bounds(bounds)
     

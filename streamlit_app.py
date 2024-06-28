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
            # Create initial map centered around the mean location of all data
            m = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=5)
            marker_cluster = folium.plugins.MarkerCluster().add_to(m)

            # Display markers for all data
            for idx, row in data.iterrows():
                # Create a popup message with site information
                popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                f"<b>Latitude:</b> {row['Lat']}<br>" \
                                f"<b>Longitude:</b> {row['Lon']}<br>"

                folium.Marker(
                    location=[row['Lat'], row['Lon']],
                    popup=folium.Popup(popup_message, max_width=400),
                    icon=folium.Icon(color='blue', icon='cloud')
                ).add_to(marker_cluster)

            # Display the map in the Streamlit app
            folium_static(m, width=900, height=700)

            # Allow user to filter by site name to navigate map
            search_site_name = st.text_input("Enter Site Name to Filter and Navigate Map:")
            if search_site_name:
                filtered_data = data[data['Site'].str.contains(search_site_name, case=False)]
                if not filtered_data.empty:
                    # Clear previous markers and update the map to center on the filtered site
                    marker_cluster.clear_layers()
                    for idx, row in filtered_data.iterrows():
                        popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                        f"<b>Latitude:</b> {row['Lat']}<br>" \
                                        f"<b>Longitude:</b> {row['Lon']}<br>"

                        folium.Marker(
                            location=[row['Lat'], row['Lon']],
                            popup=folium.Popup(popup_message, max_width=400),
                            icon=folium.Icon(color='red', icon='cloud')  # Example: Use red color for filtered sites
                        ).add_to(marker_cluster)

                    # Update the map to center on the filtered data
                    m.location = [filtered_data['Lat'].mean(), filtered_data['Lon'].mean()]
                    m.zoom_start = 10  # Zoom in to the filtered site

                    # Display the updated map in the Streamlit app
                    folium_static(m, width=900, height=700)
                else:
                    st.warning(f"No data found for Site Name containing '{search_site_name}'.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

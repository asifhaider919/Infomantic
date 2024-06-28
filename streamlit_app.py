import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

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
        if 'Lat' not in data.columns or 'Lon' not in data.columns:
            st.error("The uploaded file must contain 'Lat' and 'Lon' columns.")
        else:
            # Create a Folium map centered around the mean location of all data
            m = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=5)

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
                ).add_to(m)

            # Display the map in the Streamlit app
            st.subheader("Map of Sites")
            st_folium(m, width=900, height=700)

            # Allow user to filter by site name to navigate map
            st.sidebar.subheader("Filter by Site Name")
            search_site_name = st.sidebar.text_input("Enter Site Name to Filter and Navigate Map:")
            if search_site_name:
                filtered_data = data[data['Site'].str.contains(search_site_name, case=False)]
                if not filtered_data.empty:
                    # Display filtered data in a table
                    st.subheader(f"Filtered Data for Site Name containing '{search_site_name}'")
                    st.write(filtered_data)

                    # Create a Folium map centered around the mean location of filtered data
                    folium_map = folium.Map(location=[filtered_data['Lat'].mean(), filtered_data['Lon'].mean()], zoom_start=10)
                    
                    # Display markers for filtered data
                    for idx, row in filtered_data.iterrows():
                        popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                        f"<b>Latitude:</b> {row['Lat']}<br>" \
                                        f"<b>Longitude:</b> {row['Lon']}<br>"

                        folium.Marker(
                            location=[row['Lat'], row['Lon']],
                            popup=folium.Popup(popup_message, max_width=400),
                            icon=folium.Icon(color='blue', icon='cloud')
                        ).add_to(folium_map)

                    st.subheader(f"Filtered Map for Site Name containing '{search_site_name}'")
                    st_folium(folium_map, width=900, height=700)
                else:
                    st.warning(f"No data found for Site Name containing '{search_site_name}'.")
    
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

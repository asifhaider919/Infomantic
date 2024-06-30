import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Set page configuration
st.set_page_config(layout="wide")

# Title of the app with reduced size
st.markdown("<h2 style='text-align: center;'>Upload File to Plot Sites on Map</h2>", unsafe_allow_html=True)

# Sidebar for file upload
st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    # Save the uploaded file
    with open(f"Input_Data.{uploaded_file.name.split('.')[-1]}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.sidebar.success(f"File saved as Input_Data.{uploaded_file.name.split('.')[-1]}")
    
    try:
        # Read the uploaded file into a pandas DataFrame
        if uploaded_file.name.endswith('.xls') or uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
        
        # Ensure the required columns are present
        if 'Lat' not in data.columns or 'Lon' not in data.columns or 'Site' not in data.columns or 'Issue' not in data.columns:
            st.sidebar.error("The uploaded file must contain 'Site', 'Lat', 'Lon', and 'Issue' columns.")
        else:
            # Sidebar filter by Site Name
            st.sidebar.subheader("Filter by Site Name")
            search_site_name = st.sidebar.text_input("Enter Site Name")

            # Sidebar for issue category legend
            st.sidebar.subheader("Issue Category Legend")
            issue_categories = data['Issue'].unique()
            color_map = {issue: 'red' for issue in issue_categories}  # Default color is red
            
            for issue in issue_categories:
                st.sidebar.markdown(f"<span style='background-color: {color_map[issue]}; padding: 5px;'>{issue}</span>", unsafe_allow_html=True)

            # Create initial map centered around the mean location of all data
            m = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=7)
            
            # Define a color map for issues
            colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
            color_map = {issue: colors[i % len(colors)] for i, issue in enumerate(issue_categories)}

            for idx, row in data.iterrows():
                # Determine marker color based on issue category
                color = color_map.get(row['Issue'], 'blue')
                
                # Create a popup message with site information
                popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                f"<b>Latitude:</b> {row['Lat']}<br>" \
                                f"<b>Longitude:</b> {row['Lon']}<br>" \
                                f"<b>Issue:</b> {row['Issue']}<br>"

                folium.CircleMarker(
                    location=[row['Lat'], row['Lon']],
                    radius=6,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.4,
                    popup=folium.Popup(popup_message, max_width=400)
                ).add_to(m)
            
            # Display the map in the Streamlit app
            folium_static(m, width=900, height=700)

    except Exception as e:
        st.sidebar.error(f"An error occurred while processing the file: {e}")

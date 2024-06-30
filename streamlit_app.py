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

            # Sidebar for issue category selection
            st.sidebar.subheader("Filter by Issue Category")
            issue_categories = data['Issue'].unique()
            selected_issues = st.sidebar.multiselect("Select Issue Categories", issue_categories, default=issue_categories)
            
            # Create initial map centered around the mean location of all data
            m = folium.Map(location=[data['Lat'].mean(), data['Lon'].mean()], zoom_start=7)
            
            # Filter data based on the selected issues
            filtered_data = data[data['Issue'].isin(selected_issues)]
            
            # Further filter data based on site name if provided
            if search_site_name:
                filtered_data = filtered_data[filtered_data['Site'].str.contains(search_site_name, case=False)]
            
            # Define a color map for issues
            color_map = {issue: folium.Icon(color='blue', icon='circle') for issue in issue_categories}
            for idx, issue in enumerate(issue_categories):
                color = f"#{idx:02x}{idx:02x}{idx:02x}"  # Generate a unique color for each issue
                color_map[issue] = folium.Icon(color=color, icon='circle')
            
            for idx, row in filtered_data.iterrows():
                # Determine marker color based on issue category
                icon = color_map.get(row['Issue'], folium.Icon(color='gray', icon='circle'))
                
                # Create a popup message with site information
                popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                f"<b>Latitude:</b> {row['Lat']}<br>" \
                                f"<b>Longitude:</b> {row['Lon']}<br>" \
                                f"<b>Issue:</b> {row['Issue']}<br>"

                folium.Marker(
                    location=[row['Lat'], row['Lon']],
                    popup=folium.Popup(popup_message, max_width=400),
                    icon=icon
                ).add_to(m)
            
            # Display the map in the Streamlit app
            folium_static(m, width=900, height=700)

    except Exception as e:
        st.sidebar.error(f"An error occurred while processing the file: {e}")

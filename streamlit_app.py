import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Set page configuration
st.set_page_config(layout="wide")

# Hide default file uploader text
hide_file_upload_style = """
    <style>
    .css-1t1j96h {
        display: none;
    }
    </style>
"""
st.markdown(hide_file_upload_style, unsafe_allow_html=True)

# Custom file uploader labels
uploaded_file_site = st.sidebar.file_uploader("", type=["xlsx"], label_visibility="collapsed", help="Upload Site Info file")
uploaded_file_txn = st.sidebar.file_uploader("", type=["xlsx"], label_visibility="collapsed", help="Upload TXN Info file")

if uploaded_file_site is not None and uploaded_file_txn is not None:
    try:
        # Read the uploaded site file into a pandas DataFrame
        if uploaded_file_site.name.endswith('.xls') or uploaded_file_site.name.endswith('.xlsx'):
            site_data = pd.read_excel(uploaded_file_site)
        else:
            site_data = pd.read_csv(uploaded_file_site)
        
        # Ensure the required columns are present for site data
        if 'Lat' not in site_data.columns or 'Lon' not in site_data.columns or 'Site' not in site_data.columns:
            st.sidebar.error("The uploaded site file must contain 'Site', 'Lat', and 'Lon' columns.")
        else:
            # Define categories for the legend based on 'Issue' column
            site_categories = site_data['Issue'].unique().tolist()
                                                                                                               
            # Extend colors list to accommodate up to 10 categories
            colors = ['green', 'blue', 'red', 'purple', 'orange', 'black', 'magenta', 'yellow', 'lime', 'teal']

            # Assign light green to a specific category
            # Example: Assign 'lightgreen' to the category 'OK'
            colors[site_categories.index('OK')] = 'green'
        
            # Sidebar filter by Site Name
            search_site_name = st.sidebar.text_input("Enter Site Name")

            # Create initial map centered around the mean location of all site data
            combined_map = folium.Map(location=[site_data['Lat'].mean(), site_data['Lon'].mean()], zoom_start=7)

            # Display markers for filtered site data or all site data if not filtered
            if search_site_name:
                filtered_site_data = site_data[site_data['Site'].str.contains(search_site_name, case=False)]
                if not filtered_site_data.empty:
                    # Calculate bounds to zoom to 10km around the first filtered site
                    first_site = filtered_site_data.iloc[0]
                    bounds = [(first_site['Lat'] - 0.05, first_site['Lon'] - 0.05), 
                              (first_site['Lat'] + 0.05, first_site['Lon'] + 0.05)]
                    
                    for idx, row in site_data.iterrows():
                        # Determine marker size
                        radius = 12 if row['Site'] in filtered_site_data['Site'].values else 6

                        # Determine marker color based on 'Issue' category
                        category = row['Issue']
                        color = colors[site_categories.index(category) % len(colors)]

                        # Create a popup message with site information
                        popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                        f"<b>

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Set page configuration
st.set_page_config(layout="wide")

# Logo image URL (replace with your actual logo URL)
logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5Kj80VCFDZV3eFqa8ppMxXlhxvjkr6XQ85A&s"

# Display the logo at the top of the sidebar
st.sidebar.image(logo_url, width=200)

# Title of the app
st.title("Site and Transaction Map")

# Sidebar for file upload
uploaded_file_site = st.sidebar.file_uploader("Upload Site Excel file", type=["xlsx"])
uploaded_file_txn = st.sidebar.file_uploader("Upload TXN Excel file", type=["xlsx"])

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
            site_map = folium.Map(location=[site_data['Lat'].mean(), site_data['Lon'].mean()], zoom_start=7)

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
                                    	f"<b>SITECODE:</b> {row['SITECODE']}<br>" \
                                    	f"<b>Longitude:</b> {row['Lon']}<br>" \
                                    	f"<b>Latitude:</b> {row['Lat']}<br>" \
                                    	f"<b>Issue:</b> {row['Issue']}<br>"

                        folium.CircleMarker(
                            location=[row['Lat'], row['Lon']],
                            radius=radius,
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            popup=folium.Popup(popup_message, max_width=400)
                        ).add_to(site_map)
                    
                    # Fit the map to the bounds
                    site_map.fit_bounds(bounds)
            else:
                for idx, row in site_data.iterrows():
                    # Determine marker color based on 'Issue' category
                    category = row['Issue']
                    color = colors[site_categories.index(category) % len(colors)] if category in site_categories else 'blue'

                    # Create a popup message with site information
                    popup_message = f"<b>Site Name:</b> {row.get('Site', '')}<br>" \
                                    f"<b>SITECODE:</b> {row['SITECODE']}<br>" \
                                    f"<b>Longitude:</b> {row['Lon']}<br>" \
                                    f"<b>Latitude:</b> {row['Lat']}<br>" \
                                    f"<b>Issue:</b> {row['Issue']}<br>"

                    folium.CircleMarker(
                        location=[row['Lat'], row['Lon']],
                        radius=6,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.7,
                        popup=folium.Popup(popup_message, max_width=400)
                    ).add_to(site_map)

            # Display the legend for site data in the sidebar with colored checkboxes
            st.sidebar.subheader("Site Map Legend")
            for idx, category in enumerate(site_categories):
                color = colors[idx % len(colors)]  # Get color for category
                # Use HTML and CSS to create colored checkboxes
                st.sidebar.markdown(f'<span style="color: {color}; font-size: 1.5em">&#9632;</span> {category}', unsafe_allow_html=True)
				
            # Display the site map in the Streamlit app
            st.subheader("Site Map")
            folium_static(site_map, width=1200, height=700)
            
            # Display developer information aligned to the left and close to the map
            st.markdown("<div style='text-align: left; font-size: 14px; color: black; margin-top: 10px;'>NPO Nokia - Togo</div>", unsafe_allow_html=True)

        # Read the uploaded TXN file into a pandas DataFrame
        if uploaded_file_txn.name.endswith('.xls') or uploaded_file_txn.name.endswith('.xlsx'):
            txn_data = pd.read_excel(uploaded_file_txn)
        else:
            txn_data = pd.read_csv(uploaded_file_txn)
        
        # Check for required columns for TXN data
        required_columns_txn = ['Site_A', 'Site_B', 'Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']
        if all(col in txn_data.columns for col in required_columns_txn):
            # Convert relevant columns to numeric (in case they are not already numeric)
            numeric_columns_txn = ['Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']
            txn_data[numeric_columns_txn] = txn_data[numeric_columns_txn].apply(pd.to_numeric, errors='coerce')
            
            # Create a map centered around the mean location of the TXN data
            txn_map = folium.Map(location=[txn_data[['Lat_A', 'Lat_B']].mean().mean(), 
                                            txn_data[['Lon_A', 'Lon_B']].mean().mean()], zoom_start=7)
            
            # Iterate through rows to draw lines for TXN data
            for index, row in txn_data.iterrows():
                # Skip rows with missing or NaN values in coordinates
                if pd.isnull(row[['Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']]).any():
                    st.sidebar.warning(f"Skipping TXN row {index+1}: Missing coordinates")
                    continue
                
                # Add a line from Lat_A/Lon_A to Lat_B/Lon_B
                folium.PolyLine(locations=[(row['Lat_A'], row['Lon_A']), (row['Lat_B'], row['Lon_B'])],
                                color='blue').add_to(txn_map)
            

            # Display the TXN map in the Streamlit app
            st.subheader("Transaction Map")
            folium_static(txn_map, width=1200, height=700)
            
        else:
            st.sidebar.warning(f"Required columns {required_columns_txn} not found in the TXN file.")
    
    except Exception as e:
        st.sidebar.error(f"An error occurred while processing the file: {e}")


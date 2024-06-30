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
st.title("Combined Map for TXN and Site Data")

# Sidebar for file upload
uploaded_txn_file = st.sidebar.file_uploader("Upload TXN Excel file", type=["xlsx"])
uploaded_site_file = st.sidebar.file_uploader("Upload Site Excel file", type=["csv", "xls", "xlsx"])

# Function to draw lines from Site A to Site B (TXN Data)
def draw_lines_from_txn_data(txn_data):
    m = folium.Map(location=[txn_data[['Lat_A', 'Lat_B']].mean().mean(),
                              txn_data[['Lon_A', 'Lon_B']].mean().mean()], zoom_start=7)
    for index, row in txn_data.iterrows():
        try:
            # Convert relevant columns to numeric
            row[['Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']] = pd.to_numeric(row[['Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']], errors='coerce')
            
            # Skip rows with NaN values in coordinates
            if pd.isnull(row[['Lat_A', 'Lon_A', 'Lat_B', 'Lon_B']]).any():
                st.sidebar.warning(f"Skipping row {index + 1}: Missing coordinates")
                continue
            
            folium.PolyLine(locations=[(row['Lat_A'], row['Lon_A']), (row['Lat_B'], row['Lon_B'])],
                            color='blue').add_to(m)
        except Exception as e:
            st.sidebar.error(f"Error processing row {index + 1}: {e}")
    return m

# Function to plot markers for site data
def plot_markers_from_site_data(site_data):
    categories = site_data['Issue'].unique().tolist()
    colors = ['green', 'blue', 'red', 'purple', 'orange', 'black', 'magenta', 'yellow', 'lime', 'teal']
    m = folium.Map(location=[site_data['Lat'].mean(), site_data['Lon'].mean()], zoom_start=7)
    for idx, row in site_data.iterrows():
        try:
            # Convert relevant columns to numeric
            row[['Lat', 'Lon']] = pd.to_numeric(row[['Lat', 'Lon']], errors='coerce')
            
            # Skip rows with NaN values in coordinates
            if pd.isnull(row[['Lat', 'Lon']]).any():
                st.sidebar.warning(f"Skipping row {idx + 1}: Missing coordinates")
                continue
            
            category = row['Issue']
            color = colors[categories.index(category) % len(colors)] if category in categories else 'blue'
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
            ).add_to(m)
        except Exception as e:
            st.sidebar.error(f"Error processing row {idx + 1}: {e}")
    return m

# Main app logic based on uploaded files
if uploaded_txn_file is not None:
    try:
        txn_data = pd.read_excel(uploaded_txn_file)
        st.sidebar.success(f"File saved as {uploaded_txn_file.name}")
        st.subheader("TXN Data")
        txn_map = draw_lines_from_txn_data(txn_data)
        folium_static(txn_map, width=1200, height=700)
    except Exception as e:
        st.sidebar.error(f"Error processing TXN file: {e}")

if uploaded_site_file is not None:
    try:
        site_data = pd.read_excel(uploaded_site_file) if uploaded_site_file.name.endswith('.xlsx') else pd.read_csv(
            uploaded_site_file)
        st.sidebar.success(f"File saved as {uploaded_site_file.name}")
        st.subheader("Site Data")
        site_map = plot_markers_from_site_data(site_data)
        
        # Display the legend in the sidebar with colored checkboxes
        st.sidebar.subheader("Legend")
        for idx, category in enumerate(categories):
            color = colors[idx % len(colors)]  # Get color for category
            # Use HTML and CSS to create colored checkboxes
            st.sidebar.markdown(f'<span style="color: {color}; font-size: 1.5em">&#9632;</span> {category}', unsafe_allow_html=True)
        
        folium_static(site_map, width=1200, height=700)
        
    except Exception as e:
        st.sidebar.error(f"Error processing Site file: {e}")

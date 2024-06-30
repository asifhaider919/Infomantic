import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
from io import BytesIO

# Set page configuration
st.set_page_config(layout="wide")

# Logo image URL (replace with your actual logo URL)
logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5Kj80VCFDZV3eFqa8ppMxXlhxvjkr6XQ85A&s"

# Display the logo at the top of the sidebar
st.sidebar.image(logo_url, width=200)

# Title of the app with reduced size
st.markdown("<h2 style='text-align: left;'>Network Capacity Limitation / Frame Loss</h2>", unsafe_allow_html=True)

# Function to load default dataset from GitHub
@st.cache
def load_default_dataset():
    url = 'https://github.com/asifhaider919/Infomantic/blob/master/DataInput.xlsx'
    response = requests.get(url)
    return pd.read_excel(BytesIO(response.content))

# Sidebar for file upload
uploaded_file = st.sidebar.file_uploader("Choose a xls/xslx file", type=["csv", "xls", "xlsx"])

# Load default dataset if no file uploaded
if uploaded_file is None:
    st.sidebar.info("No file uploaded. Loading default dataset...")
    try:
        data = load_default_dataset()
    except Exception as e:
        st.sidebar.error(f"Error loading default dataset: {e}")
else:
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
        if 'Lat' not in data.columns or 'Lon' not in data.columns or 'Site' not in data.columns:
            st.sidebar.error("The uploaded file must contain 'Site', 'Lat', and 'Lon' columns.")
    except Exception as e:
        st.sidebar.error(f"An error occurred while processing the file: {e}")

# Continue with the rest of your Streamlit app code...

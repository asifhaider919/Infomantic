import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set wide layout
st.set_page_config(layout="wide")

# Sidebar for file upload
st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

# Default chart height
default_chart_height = 300

# Default date range based on DataFrame if available
date_range = None

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Convert the DateTime column to pandas datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Sidebar for controlling chart dimensions
    st.sidebar.header("Chart Settings")
    chart_width = st.sidebar.slider("Chart Width", min_value=500, max_value=3000, value=800)
    chart_height = st.sidebar.slider("Chart Height", min_value=300, max_value=1000, value=default_chart_height)

    # Determine date range from DataFrame
    if 'DateTime' in df.columns:
        date_range = (df['DateTime'].min(), df['DateTime'].max())

    # DateTime slider in the sidebar
    if date_range:
        start_date, end_date = st.sidebar.slider(
            "Select Date Range",
            min_value=datetime.date(date_range[0]),
            max_value=datetime.date(date_range[1]),
            value=(datetime.date(date_range[0]), datetime.date(date_range[1]))
        )

        # Convert start_date and end_date to datetime64[ns]
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

    else:
        st.sidebar.warning("No DateTime column found in the uploaded file.")

    # Ensure the 'items' column exists
    if 'items' in df.columns:
        # Get unique items
        items = df['items'].unique()

        # Create two columns for displaying charts side by side
        col1, col2 = st.columns(2)

        # Iterate through each metric column (starting from the 3rd column)
        for i, col in enumerate(df.columns[2:], start=1):
            # Filter data based on selec

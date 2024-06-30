import streamlit as st
import pandas as pd
import plotly.express as px

# Set wide layout
st.set_page_config(layout="wide")

# Sidebar for file upload
st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Convert the DateTime column to pandas datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Sidebar for controlling chart dimensions
    st.sidebar.header("Chart Settings")
    chart_width = st.sidebar.slider("Chart Width", min_value=500, max_value=3000, value=800)
    chart_height = st.sidebar.slider("Chart Height", min_value=300, max_value=1000, value=600)

    # Ensure the 'items' column exists
    if 'items' in df.columns:
        # Get unique items
        items = df['items'].unique()

        # Iterate through each metric column (starting from the 3rd column)
        for col in df.columns[2:]:
            # Create an interactive plot using Plotly for each metric
            fig = px.line(df, x='DateTime', y=col, color='items')
            fig.update_layout(
                xaxis_title='',
                yaxis_title='',
                width=chart_width,
                height=chart_height,

            )
            st.plotly_chart(fig)
    else:
        st.error("'items' column not found in the uploaded file. Please check the column names.")

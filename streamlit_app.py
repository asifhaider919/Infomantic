import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Metrics for Each Item')

# File upload
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Display the columns of the DataFrame for debugging
    st.write("Columns in the uploaded file:", df.columns.tolist())

    # Convert the DateTime column to pandas datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Ensure the 'items' column exists
    if 'items' in df.columns:
        # Get unique items
        items = df['items'].unique()

        # Iterate through each item and create a plot
        for item in items:
            st.header(f'Item: {item}')
            item_data = df[df['items'] == item]
            
            # Create an interactive plot using Plotly
            fig = px.line(item_data, x='DateTime', y=item_data.columns[2:], title=f'Item: {item}')
            fig.update_layout(xaxis_title='', yaxis_title='')
            st.plotly_chart(fig)
    else:
        st.error("'items' column not found in the uploaded file. Please check the column names.")

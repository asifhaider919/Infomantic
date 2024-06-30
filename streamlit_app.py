import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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
    chart_width = st.sidebar.slider("Chart Width", min_value=200, max_value=1000, value=800)
    chart_height = st.sidebar.slider("Chart Height", min_value=200, max_value=1000, value=200)

    # Sidebar for selecting metrics and items
    st.sidebar.header("Data Selection")
    
    # Ensure the 'items' column exists
    if 'items' in df.columns:
        # Multiselect dropdown for selecting metrics
        all_metrics_option = "All Metrics"
        available_metrics = df.columns[2:].tolist()

        # Checkbox to display all metrics
        display_all_metrics = st.sidebar.checkbox("Display All Metrics")

        if display_all_metrics:
            selected_metrics = available_metrics
        else:
            # Search box for filtering metrics by typing
            filter_text = st.sidebar.text_input("Filter Metrics", "")

            # Filter metrics for autocomplete suggestions
            filtered_metrics = [metric for metric in available_metrics if filter_text.lower() in metric.lower()]

            # Show autocomplete suggestions in a selectbox
            selected_metrics = st.sidebar.multiselect("Select Metrics", filtered_metrics, default=filtered_metrics)

        if len(selected_metrics) > 0:
            # Sidebar for selecting items
            selected_items = st.sidebar.multiselect("Select Items", df['items'].unique())

            if len(selected_items) > 0:
                # Prepare data for the table
                table_data = {}

                for metric in selected_metrics:
                    metric_values = []

                    for item in selected_items:
                        # Filter data based on selected metric and item
                        filtered_data = df[(df['items'] == item)]

                        # Find the last available hour for the selected metric and item
                        last_hour_data = filtered_data[filtered_data[metric].notnull()].tail(1)
                        if not last_hour_data.empty:
                            last_hour_value = last_hour_data[metric].iloc[0]
                        else:
                            last_hour_value = None

                        # Find the corresponding hour from previous days
                        previous_hour_data = filtered_data[filtered_data['DateTime'].apply(lambda x: x.hour) == last_hour_data['DateTime'].iloc[0].hour - 1]
                        if not previous_hour_data.empty:
                            previous_hour_value = previous_hour_data[metric].iloc[0]
                        else:
                            previous_hour_value = None

                        metric_values.extend([last_hour_value, previous_hour_value])

                    table_data[metric] = metric_values

                # Create DataFrame for the table
                table_df = pd.DataFrame(table_data, index=pd.Index(selected_items, name='Item'))

                # Display the table
                st.dataframe(table_df)

            else:
                st.warning("Please select at least one item.")
        else:
            st.warning("Please select at least one metric.")
    else:
        st.error("'items' column not found in the uploaded file. Please check the column names.")
else:
    st.info("Please upload an Excel file.")

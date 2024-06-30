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
default_chart_height = 200

# Default date range based on DataFrame if available
date_range = None

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Convert the DateTime column to pandas datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Sidebar for controlling chart dimensions
    st.sidebar.header("Chart Settings")
    chart_width = st.sidebar.slider("Chart Width", min_value=200, max_value=1000, value=800)
    chart_height = st.sidebar.slider("Chart Height", min_value=200, max_value=1000, value=default_chart_height)

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
        # Multiselect dropdown for selecting items
        all_items_option = "All Items"
        available_items = df['items'].unique().tolist()

        # Checkbox to display all items
        display_all_items = st.sidebar.checkbox("Display All Items")

        if display_all_items:
            selected_items = available_items
        else:
            # Search box for filtering items by typing
            filter_text = st.sidebar.text_input("Filter Items", "")

            # Filter items for autocomplete suggestions
            filtered_items = [item for item in available_items if filter_text.lower() in item.lower()]

            # Show autocomplete suggestions in a selectbox
            selected_items = st.sidebar.multiselect("Select Items", filtered_items, default=filtered_items)

        if len(selected_items) > 0:
            # Slider for vertical line position
            vertical_line_position = st.sidebar.slider(
                "Vertical Line Position",
                min_value=0,
                max_value=len(df) - 1,
                value=len(df) // 2,
                format="%d"
            )

            # Create two columns for displaying charts side by side
            col1, col2 = st.columns(2)

            # Iterate through each selected item
            for i, item in enumerate(selected_items, start=1):
                if item == all_items_option:
                    continue  # Skip "All Items" option in individual charts

                # Filter data based on selected date range and item
                filtered_df = df[(df['DateTime'] >= start_date) & (df['DateTime'] <= end_date) & (df['items'] == item)]

                # Create an interactive plot using Plotly for each item
                fig = px.line(filtered_df, x='DateTime', y='value', labels={'value': item})  # Use item name as y-axis label
                fig.update_layout(
                    xaxis_title='',
                    yaxis_title='',
                    width=chart_width,
                    height=chart_height,
                    margin=dict(l=0, r=40, t=0, b=0),  # Set margin to 40px on the right
                    paper_bgcolor='rgb(240, 240, 240)',  # Set paper background color to a lighter gray (RGB values)
                    plot_bgcolor='rgba(0,0,0,0)',   # Make plot area transparent
                    legend=dict(
                        orientation='h',  # Horizontal orientation
                        yanchor='bottom',  # Anchor legend to the bottom of the plot area
                        y=1.02,  # Adjust vertical position
                        xanchor='right',  # Anchor legend to the right of the plot area
                        x=1  # Adjust horizontal position
                    ),
                    xaxis=dict(showgrid=False, zeroline=False),  # Hide gridlines and zeroline
                    yaxis=dict(showgrid=False, zeroline=False),  # Hide gridlines and zeroline
                )

                # Add vertical line to the plot
                fig.add_vline(x=filtered_df.iloc[vertical_line_position]['DateTime'], line_width=2, line_dash="dash", line_color="red")

                # Alternate placing charts in col1 and col2
                if i % 2 == 1:
                    col1.plotly_chart(fig)
                else:
                    col2.plotly_chart(fig)

        else:
            st.warning("Please select at least one item to display.")
    else:
        st.error("'items' column not found in the uploaded file. Please check the column names.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Metrics for Each Item')

# File upload
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Convert the DateTime column to pandas datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Get unique items
    items = df['items'].unique()

    # Iterate through each item and create a plot
    for item in items:
        st.header(f'Item: {item}')
        item_data = df[df['items'] == item]
        
        plt.figure()
        for metric in df.columns[2:]:
            plt.plot(item_data['DateTime'], item_data[metric], label=metric)
        
        plt.title(f'Item: {item}')
        plt.xlabel('DateTime')
        plt.ylabel('Metrics')
        plt.legend()
        plt.grid(True)
        
        st.pyplot(plt)
        plt.clf()

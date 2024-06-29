import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'path_to_your_file.xlsx'
df = pd.read_excel(file_path)

# Convert the DateTime column to pandas datetime type
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Get unique items
items = df['items'].unique()

st.title('Metrics for Each Item')

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

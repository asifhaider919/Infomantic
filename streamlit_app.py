# Initialize lists to store data
metric_list = []
item_list = []
last_hour_list = []
previous_hour_list = []

# Iterate through each selected metric and item
for metric in selected_metrics:
    for item in selected_items:
        metric_list.append(metric)
        item_list.append(item)
        
        # Filter data based on selected metric and item
        filtered_data = df[(df['items'] == item)]
        
        # Find the last available hour for the selected metric and item
        last_hour_data = filtered_data[filtered_data[metric].notnull()].tail(1)
        if not last_hour_data.empty:
            last_hour = last_hour_data['DateTime'].iloc[0]
            
            # Find the corresponding hour from previous days
            previous_hour_data = filtered_data[filtered_data['DateTime'].apply(lambda x: x.hour) == last_hour.hour - 1]
            if not previous_hour_data.empty:
                previous_hour = previous_hour_data['DateTime'].iloc[0]
            else:
                previous_hour = None
        
        else:
            last_hour = None
            previous_hour = None
        
        # Append to respective lists
        last_hour_list.append(last_hour)
        previous_hour_list.append(previous_hour)

# Create dictionary for DataFrame
table_data = {
    "Metric": metric_list,
    "Item": item_list,
    "Last Available Hour": last_hour_list,
    "Same Hour from Previous Days": previous_hour_list
}

# Create DataFrame
table_df = pd.DataFrame(table_data)

# Display the table
st.dataframe(table_df)

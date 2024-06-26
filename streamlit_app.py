import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Define correct username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "admin"

# Title of the app
st.title("Login to Access Site Map")

# Add login components
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Check if username and password are correct
if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
    st.success("Login successful!")

    # Upload CSV file for site data
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            # Try to read the CSV file with UTF-8 encoding
            data = pd.read_csv(uploaded_file, encoding='utf-8')
            print("Columns in CSV file:", data.columns.tolist())  # Debugging: Print column names
        except UnicodeDecodeError:
            # If there's a UnicodeDecodeError, try reading with ISO-8859-1 encoding
            data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        else:
            # Check if the dataframe is empty
            if data.empty:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
            else:
                # Create a Folium map centered around the mean location of all data
                m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=5)

                # Extract distinct issues from all data and assign unique colors
                distinct_issues = data['Issue'].unique()
                issue_colors = ['red', 'blue', 'green', 'orange', 'purple']  # Define colors for issues
                issue_color_map = {issue: issue_colors[i % len(issue_colors)] for i, issue in enumerate(distinct_issues)}

                # Create a legend for the issues
                legend_html = """
                <div style="position: fixed; 
                            bottom: 50px; left: 50px; width: 150px; height: 120px; 
                            border:2px solid grey; z-index:9999; font-size:14px;
                            background-color: white;
                            ">
                            <p><b>Legend</b></p>
                """
                for issue, color in issue_color_map.items():
                    legend_html += f'<i style="background:{color}; width:10px; height:10px; display:inline-block;"></i> {issue}<br>'
                legend_html += "</div>"

                m.get_root().html.add_child(folium.Element(legend_html))

                # Display all site names on the map as markers
                for idx, row in data.iterrows():
                    # Determine color based on issue category
                    issue_color = issue_color_map.get(row['Issue'], 'blue')

                    # Create a popup message with site information and issue details
                    popup_message = f"<b>Site Name:</b> {row['SiteName']}<br>" \
                                    f"<b>Latitude:</b> {row['Latitude']}<br>" \
                                    f"<b>Longitude:</b> {row['Longitude']}<br>" \
                                    f"<b>Issue:</b> {row['Issue']}<br>"

                    folium.Marker(
                        location=[row['Latitude'], row['Longitude']],
                        popup=folium.Popup(popup_message, max_width=400),  # Increase max_width as needed
                        icon=folium.Icon(color=issue_color, icon='cloud')
                    ).add_to(m)

                # Allow user to filter by site name to navigate map
                search_site_name = st.text_input("Enter Site Name to Filter and Navigate Map:")
                if search_site_name:
                    filtered_data = data[data['SiteName'].str.contains(search_site_name, case=False)]
                    if not filtered_data.empty:
                        # Display filtered data in a table
                        st.write(filtered_data)

                        # Update map center to the filtered site location
                        site_location = [filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()]
                        m.location = site_location

                        # Clear previous markers and add filtered markers
                        for idx, row in filtered_data.iterrows():
                            issue_color = issue_color_map.get(row['Issue'], 'blue')
                            popup_message = f"<b>Site Name:</b> {row['SiteName']}<br>" \
                                            f"<b>Latitude:</b> {row['Latitude']}<br>" \
                                            f"<b>Longitude:</b> {row['Longitude']}<br>" \
                                            f"<b>Issue:</b> {row['Issue']}<br>"

                            folium.Marker(
                                location=[row['Latitude'], row['Longitude']],
                                popup=folium.Popup(popup_message, max_width=400),  # Increase max_width as needed
                                icon=folium.Icon(color=issue_color, icon='cloud')
                            ).add_to(m)

                        # Zoom in to the selected site with a 10km zoom level
                        m.fit_bounds([
                            [site_location[0] - 0.1, site_location[1] - 0.1],
                            [site_location[0] + 0.1, site_location[1] + 0.1]
                        ])

                    else:
                        st.warning(f"No data found for Site Name containing '{search_site_name}'.")

                # Display the map in the Streamlit app with increased size
                st_folium(m, width=900, height=700)
    else:
        st.info("Please upload a CSV file")
else:
    if username != "" or password != "":
        st.error("Incorrect username or password. Please try again.")

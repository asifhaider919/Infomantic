import folium

# Create a map
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

# Example markers with different icons
folium.Marker(
    location=[45.5236, -122.6750],
    popup="Portland, OR",
    icon=folium.Icon(color="blue", icon="info", prefix="fa")
).add_to(m)

folium.Marker(
    location=[45.5266, -122.6750],
    popup="Another Location",
    icon=folium.Icon(color="green", icon="star", prefix="fa")
).add_to(m)

folium.Marker(
    location=[45.5216, -122.6750],
    popup="Custom Image Marker",
    icon=folium.CustomIcon('path_to_custom_icon.png', icon_size=(32, 32))
).add_to(m)

# Display the map
m

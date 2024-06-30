import folium

# Create a map
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

# Example markers with different shapes and FontAwesome icons
folium.Marker(
    location=[45.5236, -122.6750],
    popup="Circle Marker",
    icon=folium.Icon(color="blue", icon="circle", prefix="fa")
).add_to(m)

folium.Marker(
    location=[45.5266, -122.6750],
    popup="Square Marker",
    icon=folium.Icon(color="green", icon="square", prefix="fa")
).add_to(m)

folium.Marker(
    location=[45.5216, -122.6750],
    popup="Star Marker",
    icon=folium.Icon(color="orange", icon="star", prefix="fa")
).add_to(m)

# Display the map
m

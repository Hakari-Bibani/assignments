import folium
from geopy.distance import geodesic
from IPython.display import display, HTML

# Define the coordinates
points = {
    "Point 1": (36.325735, 43.928414),
    "Point 2": (36.393432, 44.586781),
    "Point 3": (36.660477, 43.840174),
}

# Create a Folium map centered around the first point
m = folium.Map(location=points["Point 1"], zoom_start=8)

# Add markers for each point
for point, coords in points.items():
    folium.Marker(location=coords, popup=point).add_to(m)

# Calculate distances
distances = {
    "Point 1 to Point 2": geodesic(points["Point 1"], points["Point 2"]).kilometers,
    "Point 2 to Point 3": geodesic(points["Point 2"], points["Point 3"]).kilometers,
    "Point 1 to Point 3": geodesic(points["Point 1"], points["Point 3"]).kilometers,
}

# Add lines between points with distance labels
line_pairs = [
    (points["Point 1"], points["Point 2"]),
    (points["Point 2"], points["Point 3"]),
    (points["Point 1"], points["Point 3"]),
]

for (coords_a, coords_b) in line_pairs:
    folium.PolyLine([coords_a, coords_b], color='blue', weight=2.5, opacity=1).add_to(m)
    mid_point = ((coords_a[0] + coords_b[0]) / 2, (coords_a[1] + coords_b[1]) / 2)
    distance = geodesic(coords_a, coords_b).kilometers
    folium.Marker(location=mid_point,
                  popup=f"{distance:.2f} km",
                  icon=folium.Icon(color='green')).add_to(m)

# Save the map to an HTML file
map_file = "map.html"
m.save(map_file)

# Display the map using an iframe
display(HTML(f'<iframe src="{map_file}" width="700" height="500"></iframe>'))

# Create and display the distance report
distance_report = "<h3>Distance Report:</h3>"
distance_report += "<ul>" + "".join([f"<li><strong>{pair}</strong>: {distance:.2f} km</li>" for pair, distance in distances.items()]) + "</ul>"
display(HTML(distance_report))

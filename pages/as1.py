import folium
from geopy.distance import geodesic

# Coordinates
point1 = (36.325735, 43.928414)
point2 = (36.393432, 44.586781)
point3 = (36.660477, 43.840174)

# Create a map
m = folium.Map(location=point1, zoom_start=10)

# Add points to the map
folium.Marker(point1, popup="Point 1").add_to(m)
folium.Marker(point2, popup="Point 2").add_to(m)
folium.Marker(point3, popup="Point 3").add_to(m)

# Calculate distances
distance_1_2 = geodesic(point1, point2).kilometers
distance_2_3 = geodesic(point2, point3).kilometers
distance_1_3 = geodesic(point1, point3).kilometers

# Display map
m.save("map.html")

# Print distance report
print(f"Distance between Point 1 and Point 2: {distance_1_2:.2f} km")
print(f"Distance between Point 2 and Point 3: {distance_2_3:.2f} km")
print(f"Distance between Point 1 and Point 3: {distance_1_3:.2f} km")

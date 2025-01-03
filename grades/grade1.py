import re
from geopy.distance import geodesic

def calculate_grade(student_code):
    grade = 0

    # Check for required libraries
    if "import geopy" in student_code and "import folium" in student_code:
        grade += 5  # Proper library imports

    # Check for correct coordinate handling
    coordinates = [
        (36.325735, 43.928414),  # Point 1
        (36.393432, 44.586781),  # Point 2
        (36.660477, 43.840174)   # Point 3
    ]
    for coord in coordinates:
        if f"{coord[0]}" in student_code and f"{coord[1]}" in student_code:
            grade += 1.67  # Correct coordinate handling

    # Check for distance calculations
    distances = {
        "Point 1 to Point 2": 59.57,
        "Point 2 to Point 3": 73.14,
        "Point 1 to Point 3": 37.98
    }
    for pair, expected_distance in distances.items():
        if f"geodesic({coordinates[0]}, {coordinates[1]})" in student_code:
            grade += 10  # Correct implementation of geopy distance calculation
        if f"{expected_distance}" in student_code:
            grade += 6.67  # Accurate distance calculations

    # Check for map visualization
    if "folium.Map" in student_code:
        grade += 15  # Correct map generation
    if "folium.Marker" in student_code:
        grade += 15  # All three points correctly plotted
    if "folium.PolyLine" in student_code:
        grade += 10  # Proper map lines and connections

    # Ensure the grade does not exceed 100
    return min(grade, 100)

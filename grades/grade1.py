from geopy.distance import geodesic
import folium

def grade_assignment(student_code):
    # Initialize grade
    grade = 0

    # Check if required libraries are imported
    if "import folium" in student_code and "from geopy.distance import geodesic" in student_code:
        grade += 5  # Points for proper library imports

    # Check if coordinates are handled correctly
    coordinates = [
        (36.325735, 43.928414),  # Point 1
        (36.393432, 44.586781),  # Point 2
        (36.660477, 43.840174)   # Point 3
    ]
    if all(f"({lat}, {lon})" in student_code for lat, lon in coordinates):
        grade += 5  # Points for correct coordinate handling

    # Check if code runs without errors
    try:
        exec(student_code)
        grade += 10  # Points for code running without errors
    except Exception as e:
        print(f"Error executing code: {e}")

    # Check map visualization
    if "folium.Map" in student_code and "folium.Marker" in student_code and "folium.PolyLine" in student_code:
        grade += 15  # Points for correct map generation
        grade += 15  # Points for plotting all three points
        grade += 10  # Points for proper map lines and connections

    # Check distance calculations
    correct_distances = {
        (0, 1): 59.57,  # Point 1 to Point 2
        (1, 2): 73.14,  # Point 2 to Point 3
        (0, 2): 37.98   # Point 1 to Point 3
    }
    try:
        exec(student_code)
        for (i, j), correct_distance in correct_distances.items():
            calculated_distance = geodesic(coordinates[i], coordinates[j]).km
            if abs(calculated_distance - correct_distance) < 0.1:
                grade += 6.67  # Points for each correct distance calculation
    except Exception as e:
        print(f"Error calculating distances: {e}")

    return min(grade, 100)  # Ensure grade does not exceed 100

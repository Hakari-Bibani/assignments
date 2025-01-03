from geopy.distance import geodesic

def grade_assignment(student_code):
    # Initialize grade
    grade = 0

    # Check for correct library imports
    if "import folium" in student_code and "from geopy.distance import geodesic" in student_code:
        grade += 5  # Full points for correct imports

    # Check for correct coordinate handling
    coordinates = [
        (36.325735, 43.928414),  # Point 1
        (36.393432, 44.586781),  # Point 2
        (36.660477, 43.840174)   # Point 3
    ]
    if all(f"({lat}, {lon})" in student_code for lat, lon in coordinates):
        grade += 5  # Full points for correct coordinate handling

    # Check if code runs without errors
    try:
        exec(student_code)
        grade += 10  # Full points for error-free execution
    except:
        pass  # No points if code fails

    # Check for map visualization
    if "folium.Map" in student_code and "folium.Marker" in student_code:
        grade += 15  # Full points for map generation
    if "folium.PolyLine" in student_code:
        grade += 10  # Full points for map lines

    # Check for distance calculations
    correct_distances = {
        "Point 1 to Point 2": 59.57,
        "Point 2 to Point 3": 73.14,
        "Point 1 to Point 3": 37.98
    }
    if "geodesic" in student_code:
        grade += 10  # Full points for using geodesic
        for pair, distance in correct_distances.items():
            if f"{distance:.2f}" in student_code:
                grade += 6.67  # Approx 20 points for all distances

    return min(grade, 100)  # Ensure grade does not exceed 100

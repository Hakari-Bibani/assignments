def grade_assignment(student_code):
    """
    Grades the student's code based on the provided rubric.
    """
    grade = 0

    # Check for required libraries
    if "import folium" in student_code and "from geopy.distance import geodesic" in student_code:
        grade += 5  # Proper library imports

    # Check for correct coordinate handling
    coordinates = [
        (36.325735, 43.928414),  # Point 1
        (36.393432, 44.586781),  # Point 2
        (36.660477, 43.840174),  # Point 3
    ]
    for coord in coordinates:
        if f"{coord[0]}, {coord[1]}" in student_code:
            grade += 1.67  # Correct coordinate handling

    # Check for map visualization
    if "folium.Map" in student_code:
        grade += 15  # Correct map generation
    if "folium.Marker" in student_code:
        grade += 15  # All points plotted
    if "folium.PolyLine" in student_code:
        grade += 10  # Proper map lines and connections

    # Check for distance calculations
    if "geodesic" in student_code:
        grade += 10  # Correct implementation of geopy distance calculation
    if "distances" in student_code:
        grade += 20  # All distances calculated accurately

    # Ensure the grade does not exceed 100
    return min(grade, 100)

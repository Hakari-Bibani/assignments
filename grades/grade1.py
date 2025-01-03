import folium
from geopy.distance import geodesic

def grade_assignment(code_string):
    # Initialize grade
    grade = 0
    
    try:
        # Create a local namespace
        local_namespace = {}
        
        # Execute the student's code
        exec(code_string, globals(), local_namespace)
        
        # Check if required variables exist
        if 'distances' not in local_namespace or 'map_obj' not in local_namespace:
            return grade
        
        distances = local_namespace['distances']
        map_obj = local_namespace['map_obj']
        
        # Check if map object is created correctly (20 points)
        if isinstance(map_obj, folium.Map):
            grade += 20
        
        # Define correct coordinates
        points = [
            (36.325735, 43.928414),
            (36.393432, 44.586781),
            (36.660477, 43.840174)
        ]
        
        # Check if markers are present on the map (30 points)
        markers_found = 0
        for marker in map_obj._children.values():
            if isinstance(marker, folium.Marker):
                markers_found += 1
        
        if markers_found == 3:
            grade += 30
        
        # Calculate correct distances (50 points)
        correct_distances = {
            'Distance 1-2': round(geodesic(points[0], points[1]).kilometers, 2),
            'Distance 2-3': round(geodesic(points[1], points[2]).kilometers, 2),
            'Distance 1-3': round(geodesic(points[0], points[2]).kilometers, 2)
        }
        
        # Compare student's distances with correct distances
        if isinstance(distances, dict) and len(distances) == 3:
            for key in correct_distances:
                if key in distances:
                    student_dist = round(float(distances[key]), 2)
                    correct_dist = correct_distances[key]
                    # Allow for small differences due to rounding
                    if abs(student_dist - correct_dist) < 0.1:
                        grade += 50/3
        
        return round(grade)
    
    except Exception as e:
        print(f"Grading error: {str(e)}")
        return grade

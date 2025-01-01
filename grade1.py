from geopy.distance import geodesic
import ast
import re

def grade_assignment(code):
    total_points = 0
    feedback = []
    
    # Initialize coordinate points
    POINT1 = (36.325735, 43.928414)
    POINT2 = (36.393432, 44.586781)
    POINT3 = (36.660477, 43.840174)
    
    CORRECT_DISTANCES = {
        'p1_p2': 59.57,
        'p2_p3': 73.14,
        'p1_p3': 37.98
    }
    
    # 1. Code Structure and Implementation (30 points)
    try:
        # Check imports (5 points)
        required_libraries = ['geopy', 'folium']
        found_libraries = []
        import_pattern = r'import\s+(\w+)|from\s+(\w+)\s+import'
        matches = re.findall(import_pattern, code)
        for match in matches:
            lib = match[0] if match[0] else match[1]
            found_libraries.append(lib)
        
        library_points = min(5, len([lib for lib in required_libraries if any(found in lib for found in found_libraries)]) * 2.5)
        total_points += library_points
        feedback.append(f"Library imports: {library_points}/5 points")
        
        # Check coordinate handling (5 points)
        coordinate_points = 0
        if str(POINT1) in code.replace(' ', ''): coordinate_points += 1.67
        if str(POINT2) in code.replace(' ', ''): coordinate_points += 1.67
        if str(POINT3) in code.replace(' ', ''): coordinate_points += 1.67
        total_points += coordinate_points
        feedback.append(f"Coordinate handling: {coordinate_points:.2f}/5 points")
        
        # Code runs without errors (10 points)
        exec(code)
        total_points += 10
        feedback.append("Code execution: 10/10 points")
        
        # Code efficiency and best practices (10 points)
        efficiency_points = 10
        if len(code.split('\n')) > 100: efficiency_points -= 2
        if code.count('for') > 3: efficiency_points -= 2
        total_points += efficiency_points
        feedback.append(f"Code efficiency: {efficiency_points}/10 points")
        
    except Exception as e:
        feedback.append(f"Error in code execution: {str(e)}")
    
    # 2. Map Visualization (40 points)
    try:
        # Check for map generation (15 points)
        if 'folium.Map' in code:
            total_points += 15
            feedback.append("Map generation: 15/15 points")
        else:
            feedback.append("Map generation: 0/15 points - Missing folium.Map")
        
        # Check for markers (15 points)
        marker_points = 0
        if 'Marker' in code:
            marker_count = code.count('Marker')
            marker_points = min(15, marker_count * 5)
        total_points += marker_points
        feedback.append(f"Map markers: {marker_points}/15 points")
        
        # Check for polylines (10 points)
        if 'PolyLine' in code:
            total_points += 10
            feedback.append("Map connections: 10/10 points")
        else:
            feedback.append("Map connections: 0/10 points - Missing PolyLine")
        
    except Exception as e:
        feedback.append(f"Error in map evaluation: {str(e)}")
    
    # 3. Distance Calculations (30 points)
    try:
        # Check for geodesic implementation (10 points)
        if 'geodesic' in code:
            total_points += 10
            feedback.append("Distance calculation method: 10/10 points")
        else:
            feedback.append("Distance calculation method: 0/10 points - Missing geodesic")
        
        # Check distance accuracy (20 points)
        # This is a basic check - you might want to make it more sophisticated
        distance_points = 0
        for distance in CORRECT_DISTANCES.values():
            if str(round(distance, 2)) in code:
                distance_points += 6.67
        total_points += distance_points
        feedback.append(f"Distance accuracy: {distance_points:.2f}/20 points")
        
    except Exception as e:
        feedback.append(f"Error in distance evaluation: {str(e)}")
    
    return round(total_points), "\n".join(feedback)

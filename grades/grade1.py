import ast
from geopy.distance import geodesic
import re

def grade_assignment(code_submission):
    total_points = 0
    feedback = []
    
    # Initialize coordinates for distance verification
    COORDINATES = {
        'point1': (36.325735, 43.928414),
        'point2': (36.393432, 44.586781),
        'point3': (36.660477, 43.840174)
    }
    
    CORRECT_DISTANCES = {
        'p1_p2': 59.57,  # Point 1 to Point 2
        'p2_p3': 73.14,  # Point 2 to Point 3
        'p1_p3': 37.98   # Point 1 to Point 3
    }
    
    try:
        # Parse the code
        tree = ast.parse(code_submission)
        
        # 1. Code Structure and Implementation (30 points)
        
        # Check imports (5 points)
        imports = [node for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]
        required_libs = ['geopy', 'folium']
        found_libs = []
        
        for imp in imports:
            if isinstance(imp, ast.Import):
                found_libs.extend(name.name.split('.')[0] for name in imp.names)
            else:
                found_libs.append(imp.module.split('.')[0])
        
        import_score = 0
        for lib in required_libs:
            if lib in found_libs:
                import_score += 2.5
        
        total_points += import_score
        feedback.append(f"Library imports: {import_score}/5 points")
        
        # Check coordinate handling (5 points)
        coordinate_score = 0
        code_str = code_submission.lower()
        
        for coord in COORDINATES.values():
            if str(coord[0]) in code_str and str(coord[1]) in code_str:
                coordinate_score += 1.67
        
        total_points += coordinate_score
        feedback.append(f"Coordinate handling: {coordinate_score}/5 points")
        
        # Code runs without errors (10 points)
        try:
            exec(code_submission)
            total_points += 10
            feedback.append("Code execution: 10/10 points")
        except Exception as e:
            feedback.append(f"Code execution: 0/10 points - Error: {str(e)}")
        
        # Code efficiency and best practices (10 points)
        efficiency_score = 10
        
        # Check for unnecessary loops or redundant calculations
        loops = len([node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))])
        if loops > 3:  # More loops than necessary
            efficiency_score -= 2
        
        # Check variable naming
        names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
        if any(len(name) < 2 for name in names):  # Poor variable naming
            efficiency_score -= 2
        
        total_points += efficiency_score
        feedback.append(f"Code efficiency: {efficiency_score}/10 points")
        
        # 2. Map Visualization (40 points)
        
        # Check for folium map creation (15 points)
        map_score = 0
        if 'folium.Map' in code_submission:
            map_score += 15
        
        total_points += map_score
        feedback.append(f"Map generation: {map_score}/15 points")
        
        # Check for markers (15 points)
        marker_score = 0
        marker_count = code_submission.count('Marker')
        if marker_count >= 3:
            marker_score += 15
        else:
            marker_score += (marker_count * 5)
        
        total_points += marker_score
        feedback.append(f"Point plotting: {marker_score}/15 points")
        
        # Check for polylines (10 points)
        polyline_score = 0
        if 'PolyLine' in code_submission or 'polyline' in code_submission.lower():
            polyline_score += 10
        
        total_points += polyline_score
        feedback.append(f"Map connections: {polyline_score}/10 points")
        
        # 3. Distance Calculations (30 points)
        
        # Check for geodesic implementation (10 points)
        distance_score = 0
        if 'geodesic' in code_submission:
            distance_score += 10
        
        total_points += distance_score
        feedback.append(f"Distance calculation implementation: {distance_score}/10 points")
        
        # Check distance accuracy (20 points)
        accuracy_score = 0
        
        # Extract numbers that look like distances from the code
        numbers = re.findall(r'\d+\.\d+', code_submission)
        distances_found = [float(num) for num in numbers if 35 < float(num) < 75]  # Range for possible distances
        
        correct_values = list(CORRECT_DISTANCES.values())
        for dist in distances_found:
            if any(abs(dist - correct) < 0.1 for correct in correct_values):
                accuracy_score += 6.67
        
        total_points += accuracy_score
        feedback.append(f"Distance accuracy: {accuracy_score}/20 points")
        
    except Exception as e:
        feedback.append(f"Error during grading: {str(e)}")
        return 0, "\n".join(feedback)
    
    # Round total points to nearest integer
    total_points = round(total_points)
    
    return total_points, "\n".join(feedback)

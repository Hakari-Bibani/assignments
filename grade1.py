import ast
import inspect
from geopy.distance import geodesic

def check_imports(code_str):
    """Check if required libraries are imported"""
    try:
        tree = ast.parse(code_str)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(n.name for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        
        required_libs = {'geopy', 'folium'}
        found_libs = set(imports)
        
        return len(required_libs.intersection(found_libs)) * 2.5  # 5 points total
    except:
        return 0

def check_coordinates(code_str):
    """Check if coordinates are correctly specified"""
    correct_coords = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    ]
    
    try:
        tree = ast.parse(code_str)
        found_coords = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Tuple):
                if len(node.elts) == 2:
                    try:
                        lat = float(node.elts[0].value)
                        lon = float(node.elts[1].value)
                        found_coords.append((lat, lon))
                    except:
                        continue
        
        points = 0
        for coord in correct_coords:
            if any(abs(c[0] - coord[0]) < 0.0001 and abs(c[1] - coord[1]) < 0.0001 
                  for c in found_coords):
                points += 1.67
        
        return points  # 5 points total
    except:
        return 0

def check_distance_calculations(code_str):
    """Check if distances are calculated correctly"""
    correct_distances = {
        (0, 1): 59.57,  # Point 1 to Point 2
        (1, 2): 73.14,  # Point 2 to Point 3
        (0, 2): 37.98   # Point 1 to Point 3
    }
    
    try:
        # Execute code in controlled environment
        locals_dict = {}
        exec(code_str, {'geodesic': geodesic}, locals_dict)
        
        # Look for values close to correct distances
        points = 0
        for values in locals_dict.values():
            if isinstance(values, (int, float)):
                for correct_dist in correct_distances.values():
                    if abs(values - correct_dist) < 0.1:
                        points += 6.67  # 20 points total / 3 distances
        
        return min(points, 20)
    except:
        return 0

def check_map_visualization(code_str):
    """Check map visualization implementation"""
    try:
        tree = ast.parse(code_str)
        points = 0
        
        # Check for folium.Map creation
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr == 'Map':
                    points += 15
                elif hasattr(node.func, 'attr') and node.func.attr == 'Marker':
                    points += 5  # Up to 15 points for markers
                elif hasattr(node.func, 'attr') and node.func.attr == 'PolyLine':
                    points += 10
        
        return min(points, 40)  # Cap at 40 points
    except:
        return 0

def grade_assignment(code_str):
    """Main grading function"""
    total = 0
    
    # Code Structure and Implementation (30 points)
    total += check_imports(code_str)  # 5 points
    total += check_coordinates(code_str)  # 5 points
    
    try:
        exec(code_str)
        total += 10  # Code runs without errors
    except:
        pass
    
    # Code efficiency (simple check - could be improved)
    if len(code_str.split('\n')) < 50:
        total += 10
    elif len(code_str.split('\n')) < 100:
        total += 5
    
    # Map Visualization (40 points)
    total += check_map_visualization(code_str)
    
    # Distance Calculations (30 points)
    total += check_distance_calculations(code_str)
    
    return min(round(total), 100)  # Ensure total doesn't exceed 100

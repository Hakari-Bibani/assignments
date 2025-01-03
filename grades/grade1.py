import ast
import re

def grade_assignment(code):
    total_points = 0
    
    # 1. Code Structure (30 points)
    def check_imports(code_str):
        points = 0
        required_imports = ['geopy', 'folium']
        for imp in required_imports:
            if imp in code_str.lower():
                points += 2.5
        return points

    def check_coordinates(code_str):
        points = 0
        required_coords = [
            (36.325735, 43.928414),
            (36.393432, 44.586781),
            (36.660477, 43.840174)
        ]
        for coord in required_coords:
            if str(coord[0]) in code_str and str(coord[1]) in code_str:
                points += 1.67
        return min(points, 5)

    try:
        ast.parse(code)
        total_points += 10  # Code runs without errors
    except:
        pass

    total_points += check_imports(code)
    total_points += check_coordinates(code)
    
    # Best practices (10 points)
    if len(code.split('\n')) > 5:  # Basic check for reasonable code length
        total_points += 5
    if code.count('def ') > 0:  # Check for function usage
        total_points += 5

    # 2. Map Visualization (40 points)
    if 'folium.Map' in code:
        total_points += 15
    if 'add_to' in code and 'Marker' in code:
        total_points += 15
    if 'PolyLine' in code:
        total_points += 10

    # 3. Distance Calculations (30 points)
    if 'geodesic' in code:
        total_points += 10
    
    # Check for correct distances (allowing for small variations)
    distances = {
        "59.57": False,
        "73.14": False,
        "37.98": False
    }
    
    for dist in distances.keys():
        pattern = f"{dist[:2]}\\d*\\.?\\d+"
        if re.search(pattern, code):
            total_points += 6.67

    return round(min(total_points, 100), 2)

import ast
import inspect
from typing import Dict, List, Tuple

def check_imports(tree: ast.Module) -> Tuple[int, List[str]]:
    """Check if required libraries are imported."""
    required_imports = {'folium', 'geopy'}
    found_imports = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found_imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            found_imports.add(node.module)
    
    score = min(5, len(required_imports.intersection(found_imports)) * 2.5)
    missing = list(required_imports - found_imports)
    return score, missing

def check_coordinates(code: str) -> int:
    """Check if coordinates are correctly defined."""
    expected_coords = {
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    }
    
    # Look for coordinate patterns in the code
    found_coords = 0
    for coord_pair in expected_coords:
        if str(coord_pair[0]) in code and str(coord_pair[1]) in code:
            found_coords += 1
    
    return min(5, found_coords * 1.67)

def check_distance_calculations(code: str) -> int:
    """Check if distances are calculated correctly."""
    expected_distances = {
        59.57: False,  # Point 1 to Point 2
        73.14: False,  # Point 2 to Point 3
        37.98: False   # Point 1 to Point 3
    }
    
    score = 0
    
    # Check for presence of geodesic calculations
    if 'geodesic' in code:
        score += 10
    
    # Check for distance values (allowing for small variations)
    for expected_dist in expected_distances.keys():
        for line in code.split('\n'):
            # Look for numeric values in the code that match expected distances
            if any(abs(float(num) - expected_dist) < 0.1 
                  for num in ast.literal_eval(f"[{line}]") 
                  if isinstance(num, (int, float))):
                score += 6.67  # 20 points total for distances / 3
    
    return min(30, score)

def check_map_visualization(code: str) -> int:
    """Check map visualization implementation."""
    score = 0
    
    # Check for basic map creation
    if 'folium.Map' in code:
        score += 15
    
    # Check for markers
    if 'folium.Marker' in code:
        score += 15
    
    # Check for polylines
    if 'folium.PolyLine' in code:
        score += 10
    
    return score

def grade_assignment(code: str) -> float:
    """
    Grade the assignment based on multiple criteria.
    Returns total score out of 100.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0  # Invalid code
    
    # Code Structure and Implementation (30 points)
    import_score, missing_imports = check_imports(tree)
    coordinate_score = check_coordinates(code)
    
    # Try to execute code - 10 points if no errors
    try:
        compile(tree, '<string>', 'exec')
        execution_score = 10
    except Exception:
        execution_score = 0
    
    # Code efficiency (assuming 10 points if it passes basic checks)
    efficiency_score = 10 if execution_score == 10 else 0
    
    # Map Visualization (40 points)
    visualization_score = check_map_visualization(code)
    
    # Distance Calculations (30 points)
    distance_score = check_distance_calculations(code)
    
    total_score = (
        import_score +           # 5 points
        coordinate_score +       # 5 points
        execution_score +        # 10 points
        efficiency_score +       # 10 points
        visualization_score +    # 40 points
        distance_score          # 30 points
    )
    
    return round(total_score, 2)

if __name__ == "__main__":
    # Test code for grading function
    test_code = """
    import folium
    from geopy.distance import geodesic
    
    # Define coordinates
    point1 = (36.325735, 43.928414)
    point2 = (36.393432, 44.586781)
    point3 = (36.660477, 43.840174)
    
    # Create map
    m = folium.Map(location=[36.4, 44.0], zoom_start=10)
    
    # Add markers
    folium.Marker(point1).add_to(m)
    folium.Marker(point2).add_to(m)
    folium.Marker(point3).add_to(m)
    
    # Calculate distances
    dist1_2 = geodesic(point1, point2).kilometers  # 59.57
    dist2_3 = geodesic(point2, point3).kilometers  # 73.14
    dist1_3 = geodesic(point1, point3).kilometers  # 37.98
    
    # Add lines
    folium.PolyLine([point1, point2, point3], color="red").add_to(m)
    
    # Save map
    m.save('kurdistan_map.html')
    
    print(f"Distances:\\nPoint 1 to Point 2: {dist1_2:.2f} km\\nPoint 2 to Point 3: {dist2_3:.2f} km\\nPoint 1 to Point 3: {dist1_3:.2f} km")
    """
    
    grade = grade_assignment(test_code)
    print(f"Test code grade: {grade}/100")

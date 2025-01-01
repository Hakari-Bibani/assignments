import ast
import re

def check_imports(code):
    """Check if required libraries are properly imported"""
    required_imports = ['geopy', 'folium']
    score = 0
    feedback = []
    
    tree = ast.parse(code)
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    
    for lib in required_imports:
        if lib in str(imports):
            score += 2.5
            feedback.append(f"✓ {lib} correctly imported")
        else:
            feedback.append(f"✗ Missing {lib} import")
    
    return score, feedback

def check_coordinates(code):
    """Check if coordinates are correctly used"""
    coordinates = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    ]
    score = 0
    feedback = []
    
    for i, (lat, lon) in enumerate(coordinates, 1):
        lat_pattern = str(lat)[:6]  # Match first 6 digits
        lon_pattern = str(lon)[:6]  # Match first 6 digits
        if lat_pattern in code and lon_pattern in code:
            score += 1.67
            feedback.append(f"✓ Point {i} coordinates correctly used")
        else:
            feedback.append(f"✗ Point {i} coordinates not found or incorrect")
    
    return score, feedback

def check_distance_calculation(code):
    """Check distance calculations"""
    expected_distances = {
        'Point 1 to Point 2': 59.57,
        'Point 2 to Point 3': 73.14,
        'Point 1 to Point 3': 37.98
    }
    score = 0
    feedback = []
    
    # Check for geopy.distance usage
    if 'geodesic' in code or 'distance' in code:
        score += 10
        feedback.append("✓ Using geopy distance calculation")
    else:
        feedback.append("✗ Missing proper distance calculation method")
    
    # Look for distance values in the code output
    for pair, expected in expected_distances.items():
        # Allow for small variations in distance calculation
        pattern = fr"{expected:.2f}|{expected-0.1:.2f}|{expected+0.1:.2f}"
        if re.search(pattern, code):
            score += 6.67
            feedback.append(f"✓ Correct distance calculated for {pair}")
        else:
            feedback.append(f"✗ Incorrect or missing distance for {pair}")
    
    return score, feedback

def check_map_visualization(code):
    """Check map visualization implementation"""
    score = 0
    feedback = []
    
    # Check for basic folium map creation
    if 'folium.Map' in code:
        score += 15
        feedback.append("✓ Basic map creation implemented")
    else:
        feedback.append("✗ Missing map creation")
    
    # Check for markers
    if 'folium.Marker' in code:
        score += 15
        feedback.append("✓ Map markers implemented")
    else:
        feedback.append("✗ Missing map markers")
    
    # Check for connecting lines
    if 'folium.PolyLine' in code:
        score += 10
        feedback.append("✓ Connecting lines implemented")
    else:
        feedback.append("✗ Missing connecting lines between points")
    
    return score, feedback

def grade_assignment(code_submission):
    """Main grading function"""
    feedback = {}
    total_score = 0
    
    # Check imports (5 points)
    import_score, import_feedback = check_imports(code_submission)
    feedback["Library Imports"] = import_feedback
    total_score += import_score
    
    # Check coordinates (5 points)
    coord_score, coord_feedback = check_coordinates(code_submission)
    feedback["Coordinate Implementation"] = coord_feedback
    total_score += coord_score
    
    # Check map visualization (40 points)
    map_score, map_feedback = check_map_visualization(code_submission)
    feedback["Map Visualization"] = map_feedback
    total_score += map_score
    
    # Check distance calculations (30 points)
    dist_score, dist_feedback = check_distance_calculation(code_submission)
    feedback["Distance Calculations"] = dist_feedback
    total_score += dist_score
    
    # Add points for code running without errors (10 points)
    try:
        compile(code_submission, '<string>', 'exec')
        total_score += 10
        feedback["Code Execution"] = ["✓ Code compiles without syntax errors"]
    except Exception as e:
        feedback["Code Execution"] = [f"✗ Code contains syntax errors: {str(e)}"]
    
    # Code efficiency (10 points) - basic check
    if len(code_submission.split('\n')) < 100:  # Simple metric
        total_score += 10
        feedback["Code Efficiency"] = ["✓ Code is concise and well-structured"]
    else:
        feedback["Code Efficiency"] = ["✗ Code could be more efficient"]
    
    return round(total_score), feedback

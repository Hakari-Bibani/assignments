import ast
import re

def check_imports(code):
    """Check if required libraries are properly imported"""
    required_libs = ['geopy', 'folium']
    score = 0
    feedback = []
    
    try:
        tree = ast.parse(code)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(name.name.split('.')[0] for name in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module.split('.')[0])
        
        for lib in required_libs:
            if lib in imports:
                score += 2.5
                feedback.append(f"✓ {lib} correctly imported")
            else:
                feedback.append(f"✗ Missing {lib} import")
                
    except SyntaxError:
        feedback.append("✗ Syntax error in imports")
        return 0, feedback
        
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
    
    for lat, lon in coordinates:
        if str(lat) in code and str(lon) in code:
            score += 1.67
            feedback.append(f"✓ Found coordinates ({lat}, {lon})")
        else:
            feedback.append(f"✗ Missing coordinates ({lat}, {lon})")
            
    return score, feedback

def check_map_visualization(code):
    """Check map visualization implementation"""
    score = 0
    feedback = []
    
    # Check for folium map creation
    if "folium.Map" in code:
        score += 15
        feedback.append("✓ Folium map correctly initialized")
    else:
        feedback.append("✗ Missing folium map initialization")
    
    # Check for markers
    if "folium.Marker" in code:
        score += 15
        feedback.append("✓ Markers implemented correctly")
    else:
        feedback.append("✗ Missing markers implementation")
    
    # Check for polylines
    if "folium.PolyLine" in code or "folium.polyline" in code:
        score += 10
        feedback.append("✓ Polylines implemented correctly")
    else:
        feedback.append("✗ Missing polylines implementation")
    
    return score, feedback

def check_distance_calculations(code):
    """Check distance calculations implementation"""
    score = 0
    feedback = []
    
    expected_distances = {
        "Point 1 to Point 2": 59.57,
        "Point 2 to Point 3": 73.14,
        "Point 1 to Point 3": 37.98
    }
    
    # Check for geodesic usage
    if "geodesic" in code:
        score += 10
        feedback.append("✓ Geodesic distance calculation implemented")
    else:
        feedback.append("✗ Missing geodesic distance calculation")
    
    # Look for distance values in the code
    for description, expected in expected_distances.items():
        # Look for numbers that are close to the expected value
        pattern = f"{expected:.2f}|{expected:.1f}|{expected:.0f}"
        if re.search(pattern, code):
            score += 6.67
            feedback.append(f"✓ Correct distance calculation for {description}")
        else:
            feedback.append(f"✗ Incorrect or missing distance calculation for {description}")
    
    return score, feedback

def grade_submission(code):
    """Main grading function"""
    total_score = 0
    all_feedback = []
    
    # Code Structure and Implementation (30 points)
    import_score, import_feedback = check_imports(code)
    coord_score, coord_feedback = check_coordinates(code)
    
    # Run without errors worth 10 points - checked in week1.py during execution
    code_structure_score = import_score + coord_score
    if code_structure_score > 30:
        code_structure_score = 30
        
    all_feedback.extend(["### Code Structure and Implementation ###"])
    all_feedback.extend(import_feedback)
    all_feedback.extend(coord_feedback)
    
    # Map Visualization (40 points)
    map_score, map_feedback = check_map_visualization(code)
    all_feedback.extend(["\n### Map Visualization ###"])
    all_feedback.extend(map_feedback)
    
    # Distance Calculations (30 points)
    dist_score, dist_feedback = check_distance_calculations(code)
    all_feedback.extend(["\n### Distance Calculations ###"])
    all_feedback.extend(dist_feedback)
    
    total_score = code_structure_score + map_score + dist_score
    
    # Round to 2 decimal places
    total_score = round(total_score, 2)
    
    return total_score, "\n".join(all_feedback)

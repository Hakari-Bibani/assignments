def grade_assignment(code):
    total_points = 0
    feedback = []
    
    # Check for required imports
    import_points = 0
    required_imports = ['folium', 'geopy']
    for imp in required_imports:
        if imp in code:
            import_points += 2.5
            feedback.append(f"✓ Found {imp} import")
        else:
            feedback.append(f"✗ Missing {imp} import")
    total_points += import_points
    
    # Check coordinates
    coord_points = 0
    required_coords = [
        "36.325735", "43.928414",  # Point 1
        "36.393432", "44.586781",  # Point 2
        "36.660477", "43.840174"   # Point 3
    ]
    for coord in required_coords:
        if coord in code:
            coord_points += 0.83
            
    total_points += min(coord_points, 5)
    
    # Check for basic code structure
    if "folium.Map" in code:
        total_points += 15
        feedback.append("✓ Map initialization found")
    else:
        feedback.append("✗ Missing map initialization")
        
    if "folium.Marker" in code:
        total_points += 15
        feedback.append("✓ Markers implementation found")
    else:
        feedback.append("✗ Missing markers")
        
    if "PolyLine" in code or "polyline" in code:
        total_points += 10
        feedback.append("✓ Found polyline implementation")
    else:
        feedback.append("✗ Missing polylines between points")
    
    # Check for distance calculations
    if "geodesic" in code:
        total_points += 10
        feedback.append("✓ Found geodesic distance calculation")
    else:
        feedback.append("✗ Missing geodesic distance calculation")
    
    # Execute code to check distances
    try:
        # Create a safe environment to execute the code
        local_vars = {}
        exec(code, {}, local_vars)
        
        # Check if distances are close to expected values
        expected_distances = {
            "1-2": 59.57,
            "2-3": 73.14,
            "1-3": 37.98
        }
        
        distance_points = 0
        for dist_name, expected in expected_distances.items():
            # Look for any variable containing a number close to the expected distance
            found = False
            for var_name, value in local_vars.items():
                if isinstance(value, (int, float)):
                    if abs(value - expected) < 0.1:  # Allow 0.1 km tolerance
                        distance_points += 6.67
                        found = True
                        break
            
            if found:
                feedback.append(f"✓ Correct distance calculation for points {dist_name}")
            else:
                feedback.append(f"✗ Incorrect or missing distance calculation for points {dist_name}")
        
        total_points += min(distance_points, 20)
        
    except Exception as e:
        feedback.append(f"Error executing code: {str(e)}")
    
    # Code efficiency and best practices (10 points)
    if len(code.split('\n')) < 50:  # Reasonable length
        total_points += 5
    if code.count('    ') > code.count('\t'):  # Proper indentation
        total_points += 5
    
    return round(total_points), '\n'.join(feedback)

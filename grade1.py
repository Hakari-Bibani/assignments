def grade_assignment(code):
    total_points = 0
    
    # 1. Code Structure and Implementation (30 points)
    try:
        # Check for proper library imports (5 points)
        if all(lib in code for lib in ['geopy', 'folium']):
            total_points += 5
        
        # Check for correct coordinate handling (5 points)
        coordinates = [
            "36.325735, 43.928414",
            "36.393432, 44.586781",
            "36.660477, 43.840174"
        ]
        coord_points = sum(1.67 for coord in coordinates if coord in code)
        total_points += min(coord_points, 5)
        
        # Code runs without errors (10 points)
        exec(code)
        total_points += 10
        
        # Code efficiency and best practices (10 points)
        # Check for basic code quality indicators
        if (code.count('def') > 0 and  # Has functions
            code.count('\n') > 5 and    # Multiple lines
            not 'print' in code.lower()  # Uses proper output methods
           ):
            total_points += 10
            
    except Exception:
        # If code fails to run, only award points for visible elements
        pass
    
    # 2. Map Visualization (40 points)
    if 'folium.Map' in code:
        total_points += 15  # Correct map generation
        
    if 'folium.Marker' in code:
        total_points += 15  # Points plotted
        
    if 'folium.PolyLine' in code:
        total_points += 10  # Proper map lines
    
    # 3. Distance Calculations (30 points)
    if 'geodesic' in code:
        total_points += 10  # Correct implementation of geopy
        
    # Check for correct distances (20 points)
    expected_distances = [59.57, 73.14, 37.98]
    for dist in expected_distances:
        if str(round(dist, 2)) in code:
            total_points += 6.67
    
    return round(min(total_points, 100))

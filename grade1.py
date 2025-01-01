def grade_assignment(code):
    total_points = 0
    
    # 1. Code Structure and Implementation (30 points)
    try:
        # Check imports (5 points)
        if all(lib in code for lib in ['import folium', 'from geopy.distance import geodesic']):
            total_points += 5
            
        # Check coordinates (5 points)
        coordinates = [
            (36.325735, 43.928414),
            (36.393432, 44.586781),
            (36.660477, 43.840174)
        ]
        coords_found = all(str(coord[0]) in code and str(coord[1]) in code for coord in coordinates)
        if coords_found:
            total_points += 5
            
        # Code runs without errors (10 points)
        try:
            exec(code)
            total_points += 10
        except:
            pass
        
        # Code efficiency (10 points)
        if len(code.split('\n')) < 50 and 'folium.Map' in code and 'geodesic' in code:
            total_points += 10
            
    except:
        pass
        
    # 2. Map Visualization (40 points)
    try:
        if 'folium.Map' in code:
            total_points += 15  # Base map
        if 'folium.Marker' in code or 'add_to' in code:
            total_points += 15  # Points plotted
        if 'PolyLine' in code:
            total_points += 10  # Connections
    except:
        pass
        
    # 3. Distance Calculations (30 points)
    try:
        expected_distances = {
            "1-2": 59.57,
            "2-3": 73.14,
            "1-3": 37.98
        }
        
        # Check for geodesic implementation
        if 'geodesic' in code:
            total_points += 10
            
        # Check output for correct distances
        local_vars = {}
        exec(code, {}, local_vars)
        output_str = str(local_vars.get('output', ''))
        
        correct_distances = 0
        for dist in expected_distances.values():
            if str(round(dist, 2)) in output_str:
                correct_distances += 1
                
        total_points += (correct_distances * 6.67)  # Up to 20 points for correct distances
            
    except:
        pass
        
    return round(total_points)

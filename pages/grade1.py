import ast
import re

def grade_assignment(code):
    total_points = 0
    
    # 1. Code Structure and Implementation (30 points)
    try:
        # Check imports (5 points)
        if all(lib in code for lib in ['folium', 'geopy', 'geodesic']):
            total_points += 5
        
        # Check coordinate handling (5 points)
        coordinates = [
            (36.325735, 43.928414),
            (36.393432, 44.586781),
            (36.660477, 43.840174)
        ]
        coords_found = 0
        for lat, lon in coordinates:
            if str(lat) in code and str(lon) in code:
                coords_found += 1
        total_points += (coords_found * 1.67)
        
        # Code runs without errors (10 points)
        try:
            ast.parse(code)
            total_points += 10
        except:
            pass
        
        # Code efficiency and best practices (10 points)
        if (code.count('\n') < 100 and  # Not too verbose
            code.count('    ') > 5):     # Proper indentation
            total_points += 10
            
    except:
        pass
    
    # 2. Map Visualization (40 points)
    try:
        # Correct map generation (15 points)
        if 'folium.Map' in code:
            total_points += 15
        
        # Points plotted (15 points)
        markers_count = code.count('Marker(')
        total_points += min(markers_count * 5, 15)
        
        # Map lines (10 points)
        if 'PolyLine' in code:
            total_points += 10
            
    except:
        pass
    
    # 3. Distance Calculations (30 points)
    try:
        # Correct implementation (10 points)
        if 'geodesic' in code:
            total_points += 10
        
        # Distance accuracy (20 points)
        expected_distances = [59.57, 73.14, 37.98]
        for dist in expected_distances:
            if str(round(dist, 2)) in code:
                total_points += 6.67
                
    except:
        pass
    
    return round(total_points)

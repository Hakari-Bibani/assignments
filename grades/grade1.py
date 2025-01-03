import ast
import re

def grade_assignment(code):
    total_points = 0
    feedback = []
    
    # Code Structure and Implementation (30 points)
    structure_points = grade_structure(code)
    total_points += structure_points
    
    # Map Visualization (40 points)
    vis_points = grade_visualization(code)
    total_points += vis_points
    
    # Distance Calculations (30 points)
    calc_points = grade_calculations(code)
    total_points += calc_points
    
    return total_points, "\n".join(feedback)

def grade_structure(code):
    points = 0
    
    # Check imports (5 points)
    if all(lib in code for lib in ['geopy', 'folium']):
        points += 5
    
    # Check coordinate handling (5 points)
    coordinates = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    ]
    coord_points = 0
    for coord in coordinates:
        if str(coord[0]) in code and str(coord[1]) in code:
            coord_points += 1.67
    points += min(5, coord_points)
    
    # Code runs without errors (10 points)
    try:
        compile(code, '<string>', 'exec')
        points += 10
    except:
        pass
    
    # Code efficiency (10 points)
    if len(code.split('\n')) < 50 and 'def' in code:
        points += 10
    elif 'def' in code:
        points += 5
        
    return min(30, points)

def grade_visualization(code):
    points = 0
    
    # Check map generation (15 points)
    if 'folium.Map' in code:
        points += 15
    
    # Check markers (15 points)
    if 'folium.Marker' in code and code.count('Marker') >= 3:
        points += 15
    
    # Check polylines (10 points)
    if 'PolyLine' in code or 'polyline' in code:
        points += 10
        
    return min(40, points)

def grade_calculations(code):
    points = 0
    expected_distances = {
        (1, 2): 59.57,
        (2, 3): 73.14,
        (1, 3): 37.98
    }
    
    # Check geopy implementation (10 points)
    if 'geodesic' in code:
        points += 10
    
    # Check distance calculations (20 points)
    for distance in expected_distances.values():
        if str(round(distance, 2)) in code:
            points += 6.67
            
    return min(30, points)


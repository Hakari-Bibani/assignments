import ast
import re

def calculate_grade(code_submission):
    grades = {
        'code_structure': 0,  # Out of 30
        'visualization': 0,   # Out of 40
        'calculations': 0,    # Out of 30
        'total_grade': 0
    }
    
    # Check library imports (5 points)
    required_libraries = ['geopy', 'folium']
    for lib in required_libraries:
        if lib in code_submission:
            grades['code_structure'] += 2.5

    # Check coordinate handling (5 points)
    coordinates = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    ]
    
    for coord in coordinates:
        if str(coord[0]) in code_submission and str(coord[1]) in code_submission:
            grades['code_structure'] += 1.67

    # Check for code execution (10 points)
    try:
        ast.parse(code_submission)
        grades['code_structure'] += 10
    except:
        pass

    # Code efficiency and best practices (10 points)
    if len(code_submission.split('\n')) < 100:  # Reasonable length
        grades['code_structure'] += 5
    if code_submission.count('def ') >= 1:  # Function usage
        grades['code_structure'] += 5

    # Map visualization checks (40 points)
    if 'folium.Map' in code_submission:
        grades['visualization'] += 15
    if 'add_to(m)' in code_submission or 'add_to(map)' in code_submission:
        grades['visualization'] += 15
    if 'PolyLine' in code_submission:
        grades['visualization'] += 10

    # Distance calculations (30 points)
    if 'geodesic' in code_submission:
        grades['calculations'] += 10
    
    # Check for correct distances (20 points)
    correct_distances = [59.57, 73.14, 37.98]
    for distance in correct_distances:
        if str(round(distance, 2)) in code_submission:
            grades['calculations'] += 6.67

    # Calculate total grade
    grades['total_grade'] = sum([
        grades['code_structure'],
        grades['visualization'],
        grades['calculations']
    ])
    
    # Round all grades
    for key in grades:
        grades[key] = round(grades[key], 2)
    
    return grades

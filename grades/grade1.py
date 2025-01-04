import pandas as pd
from geopy.distance import geodesic
import folium
import ast
import re

# Constants
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

CORRECT_DISTANCES = {
    "1-2": 59.57,  # Point 1 to Point 2
    "2-3": 73.14,  # Point 2 to Point 3
    "1-3": 37.98   # Point 1 to Point 3
}

def check_imports(code):
    """Check for required library imports (5 points)"""
    required_imports = ['folium', 'geopy', 'geodesic']
    score = 0
    for imp in required_imports:
        if re.search(rf'\b{imp}\b', code):
            score += 5/len(required_imports)
    return score

def check_coordinates(code):
    """Check coordinate handling (5 points)"""
    score = 0
    try:
        # Look for coordinate definitions in the code
        coord_pattern = r'\(\s*36\.\d+\s*,\s*4[34]\.\d+\s*\)'
        coords_found = re.findall(coord_pattern, code)
        
        # Award points for each correct coordinate pair
        score = min(5, len(coords_found) * 1.67)
    except Exception:
        pass
    return score

def check_code_execution(code):
    """Check if code runs without errors (10 points)"""
    try:
        exec(code, {'folium': folium, 'geodesic': geodesic})
        return 10
    except Exception:
        return 0

def check_code_quality(code):
    """Evaluate code efficiency and best practices (10 points)"""
    score = 10
    
    # Check for proper variable names
    if re.search(r'\b[a-z]\b', code):  # Single letter variables
        score -= 2
        
    # Check for proper spacing
    if not re.search(r'=\s', code):  # No space after =
        score -= 2
        
    # Check for comments
    if not re.search(r'#', code):  # No comments
        score -= 2
        
    # Check for proper line spacing
    if not re.search(r'\n\s*\n', code):  # No blank lines
        score -= 2
        
    return max(0, score)

def check_map_generation(code):
    """Check map visualization (40 points total)"""
    score = 0
    
    # Check for folium.Map initialization (15 points)
    if re.search(r'folium\.Map\s*\(', code):
        score += 15
    
    # Check for markers (15 points)
    marker_count = len(re.findall(r'Marker\s*\(', code))
    score += min(15, marker_count * 5)  # 5 points per marker, max 15
    
    # Check for polylines (10 points)
    if re.search(r'(PolyLine|add_to)\s*\(', code):
        score += 10
        
    return score

def check_distance_calculations(code, exec_globals):
    """Check distance calculations (30 points total)"""
    score = 0
    
    # Check for proper geodesic implementation (10 points)
    if re.search(r'geodesic\s*\(.*\)\.kilometers', code):
        score += 10
    
    # Check distance accuracy (20 points)
    try:
        # Execute student code
        exec(code, exec_globals)
        
        # Look for distances in the output
        distances_found = False
        tolerance = 0.1  # 100 meter tolerance
        
        # Try to find distance calculations in different formats
        for var_name, var_value in exec_globals.items():
            if isinstance(var_value, (tuple, list, dict)):
                try:
                    if isinstance(var_value, dict):
                        distances = list(var_value.values())
                    else:
                        distances = list(var_value)
                        
                    if len(distances) == 3:
                        distances_found = True
                        correct_distances = [
                            CORRECT_DISTANCES["1-2"],
                            CORRECT_DISTANCES["2-3"],
                            CORRECT_DISTANCES["1-3"]
                        ]
                        
                        # Check each distance
                        for student_dist, correct_dist in zip(distances, correct_distances):
                            if isinstance(student_dist, (int, float)):
                                if abs(float(student_dist) - correct_dist) <= tolerance:
                                    score += 20/3  # 6.67 points per correct distance
                                    
                except (TypeError, ValueError):
                    continue
                    
        if not distances_found:
            score = 0
            
    except Exception:
        score = 0
        
    return score

def grade_submission(student_code):
    """
    Grade the student submission based on multiple criteria.
    Returns a score out of 100 and a breakdown of points.
    """
    try:
        exec_globals = {
            'folium': folium,
            'geodesic': geodesic
        }
        
        # Initialize scoring components
        scores = {
            "Code Structure": {
                "Imports": check_imports(student_code),
                "Coordinates": check_coordinates(student_code),
                "Execution": check_code_execution(student_code),
                "Code Quality": check_code_quality(student_code)
            },
            "Map Visualization": check_map_generation(student_code),
            "Distance Calculations": check_distance_calculations(student_code, exec_globals)
        }
        
        # Calculate total score
        total_score = (
            sum(scores["Code Structure"].values()) +
            scores["Map Visualization"] +
            scores["Distance Calculations"]
        )
        
        return round(total_score), scores
        
    except Exception as e:
        return 0, {"Error": str(e)}

if __name__ == "__main__":
    try:
        submissions = pd.read_csv("grades/data_submission.csv")
        
        # Grade each submission and store detailed results
        grades = []
        details = []
        
        for code in submissions["Assignment 1"]:
            score, breakdown = grade_submission(code)
            grades.append(score)
            details.append(breakdown)
            
        submissions["Grade"] = grades
        submissions["Grading_Details"] = details
        submissions.to_csv("grades/data_submission.csv", index=False)
        print("Grading completed successfully.")
        
    except FileNotFoundError:
        print("No submissions found.")
    except Exception as e:
        print(f"Error during grading: {e}")

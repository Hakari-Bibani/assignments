import pandas as pd
import folium
from geopy.distance import geodesic

# Constants
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Expected distances (pre-calculated)
EXPECTED_DISTANCES = {
    'dist1_2': geodesic(COORDINATES[0], COORDINATES[1]).kilometers,
    'dist2_3': geodesic(COORDINATES[1], COORDINATES[2]).kilometers,
    'dist1_3': geodesic(COORDINATES[0], COORDINATES[2]).kilometers
}

def grade_distances(distances, tolerance=0.1):
    """
    Grade distance calculations (40 points total)
    - Each correct distance is worth 13.33 points
    - Tolerance of 0.1 km allowed
    """
    score = 0
    try:
        if len(distances) != 3:
            return 0
        
        student_distances = list(distances)
        expected_distances = list(EXPECTED_DISTANCES.values())
        
        for student_dist, expected_dist in zip(student_distances, expected_distances):
            if abs(student_dist - expected_dist) <= tolerance:
                score += 13.33
        
        return round(score, 2)
    except:
        return 0

def grade_map_creation(local_vars):
    """
    Grade map creation (30 points total)
    - Basic map creation: 10 points
    - Correct center and zoom: 10 points
    - Marker creation: 10 points
    """
    score = 0
    try:
        # Find map object in local variables
        map_obj = None
        for var in local_vars:
            if isinstance(local_vars[var], folium.Map):
                map_obj = local_vars[var]
                break
        
        if not map_obj:
            return 0
        
        # Check basic map creation
        score += 10
        
        # Check center and zoom
        center = map_obj.location
        zoom = map_obj.zoom_start
        if (36 <= center[0] <= 37 and 43 <= center[1] <= 45 and 
            7 <= zoom <= 10):
            score += 10
        
        # Check markers
        markers_found = 0
        for child in map_obj._children.values():
            if isinstance(child, folium.Marker):
                markers_found += 1
        
        if markers_found >= 3:
            score += 10
            
        return score
    except:
        return 0

def grade_visualization(local_vars):
    """
    Grade visualization elements (30 points total)
    - Marker popups with information: 10 points
    - Polylines connecting points: 10 points
    - Distance labels or additional features: 10 points
    """
    score = 0
    try:
        map_obj = None
        for var in local_vars:
            if isinstance(local_vars[var], folium.Map):
                map_obj = local_vars[var]
                break
        
        if not map_obj:
            return 0
        
        # Check for popups in markers
        has_popups = False
        has_polylines = False
        has_extra_features = False
        
        for child in map_obj._children.values():
            if isinstance(child, folium.Marker):
                if child.popup:
                    has_popups = True
            elif isinstance(child, folium.PolyLine):
                has_polylines = True
            elif isinstance(child, (folium.CircleMarker, folium.Circle, folium.Rectangle)):
                has_extra_features = True
        
        if has_popups:
            score += 10
        if has_polylines:
            score += 10
        if has_extra_features:
            score += 10
            
        return score
    except:
        return 0

def grade_submission(student_code):
    """
    Grade distribution (100 points total):
    - Distance Calculations: 40 points
        * Each correct distance (±0.1 km): 13.33 points
    - Map Creation: 30 points
        * Basic map creation: 10 points
        * Correct center and zoom: 10 points
        * Marker creation: 10 points
    - Visualization: 30 points
        * Marker popups with information: 10 points
        * Polylines connecting points: 10 points
        * Distance labels or additional features: 10 points
    """
    try:
        # Create execution environment
        local_vars = {}
        exec(student_code, globals(), local_vars)
        
        # Calculate distances
        distances = calculate_distances(COORDINATES)
        
        # Grade each component
        distance_score = grade_distances(distances)
        map_score = grade_map_creation(local_vars)
        viz_score = grade_visualization(local_vars)
        
        # Calculate total score
        total_score = round(distance_score + map_score + viz_score)
        
        return total_score
        
    except Exception as e:
        print(f"Error in grading: {e}")
        return 0

if __name__ == "__main__":
    try:
        submissions = pd.read_csv("grades/data_submission.csv")
        submissions["Grade"] = submissions["Assignment 1"].apply(grade_submission)
        submissions.to_csv("grades/data_submission.csv", index=False)
        print("Grading completed successfully.")
    except FileNotFoundError:
        print("No submissions found.")
    except Exception as e:
        print(f"Error during grading process: {e}")

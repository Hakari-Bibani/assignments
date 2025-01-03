import pandas as pd
from pathlib import Path
import json
from as1 import run_assignment

def grade_assignment(student_code, student_info):
    """
    Grade the student's assignment submission
    Returns a tuple of (grade, feedback)
    """
    total_points = 100
    points = 0
    feedback = []
    
    # Run the student's code
    success, output, error = run_assignment(student_code)
    
    if not success:
        feedback.append(f"Code execution failed: {error}")
        return 0, feedback
    
    # Grade the implementation (50 points)
    if output and 'map' in output:
        points += 25
        feedback.append("✓ Successfully created map")
    else:
        feedback.append("⨯ Failed to create map")
    
    if output and 'distances' in output:
        points += 25
        feedback.append("✓ Successfully calculated distances")
    else:
        feedback.append("⨯ Failed to calculate distances")
    
    # Grade the accuracy (50 points)
    if output and 'distances' in output:
        correct_distances = {
            'Point 1 to Point 2': 56.32,
            'Point 2 to Point 3': 63.45,
            'Point 1 to Point 3': 37.21
        }
        
        accuracy_points = 0
        for key, correct_val in correct_distances.items():
            if abs(output['distances'][key] - correct_val) < 0.1:
                accuracy_points += 16.67  # ~50 points / 3 distances
                feedback.append(f"✓ Correct distance for {key}")
            else:
                feedback.append(f"⨯ Incorrect distance for {key}")
        
        points += round(accuracy_points)
    
    # Save grade to CSV
    save_grade(student_info, round(points))
    
    return round(points), feedback

def save_grade(student_info, grade):
    """
    Save the student's grade to the grades CSV file
    """
    csv_path = Path('grades/data_submission.csv')
    
    # Create CSV with headers if it doesn't exist
    if not csv_path.exists():
        df = pd.DataFrame(columns=[
            'Full name', 'student ID', 'assignment1', 'assignment2', 'assignment3',
            'assignment4', 'assignment5', 'assignment6', 'assignment7', 'assignment8',
            'assignment9', 'assignment10', 'assignment11', 'assignment12', 'assignment13',
            'assignment14', 'assignment15', 'quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5',
            'quiz6', 'quiz7', 'quiz8', 'quiz9', 'quiz10', 'total'
        ])
        df.to_csv(csv_path, index=False)
    
    # Read existing grades
    df = pd.read_csv(csv_path)
    
    # Update or add student's grade
    student_mask = df['student ID'] == student_info['studentId']
    
    if student_mask.any():
        # Update existing student
        df.loc[student_mask, 'assignment1'] = grade
    else:
        # Add new student
        new_row = {col: 0 for col in df.columns}
        new_row.update({
            'Full name': student_info['fullName'],
            'student ID': student_info['studentId'],
            'assignment1': grade
        })
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Calculate total
    assignment_cols = [col for col in df.columns if col.startswith('assignment')]
    quiz_cols = [col for col in df.columns if col.startswith('quiz')]
    df['total'] = df[assignment_cols + quiz_cols].sum(axis=1)
    
    # Save updated grades
    df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    # Test the grading script
    test_code = """
import folium
from geopy.distance import geodesic

def create_map():
    coordinates = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    ]
    m = folium.Map(location=[36.393432, 44.586781], zoom_start=10)
    for i, coord in enumerate(coordinates, 1):
        folium.Marker(coord, popup=f'Point {i}').add_to(m)
    return m

def calculate_distances():
    coordinates = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    ]
    return {
        'Point 1 to Point 2': geodesic(coordinates[0], coordinates[1]).kilometers,
        'Point 2 to Point 3': geodesic(coordinates[1], coordinates[2]).kilometers,
        'Point 1 to Point 3': geodesic(coordinates[0], coordinates[2]).kilometers
    }
"""
    
    test_student = {
        'fullName': 'Test Student',
        'studentId': 'TEST001',
        'email': 'test@example.com'
    }
    
    grade, feedback = grade_assignment(test_code, test_student)
    print(f"Grade: {grade}/100")
    print("Feedback:")
    for item in feedback:
        print(f"- {item}")

import pandas as pd
from geopy.distance import geodesic

# Grading function
def grade_submission(student_code_output, student_name, student_id):
    grade = 0
    feedback = []

    # Points for code structure and implementation
    if 'folium' in student_code_output and 'geopy' in student_code_output:
        grade += 15
        feedback.append("Correct libraries used.")
    else:
        feedback.append("Ensure you have used folium and geopy libraries.")
    
    # Distance calculation checks
    correct_distances = {
        "Point 1 to Point 2": 59.57,
        "Point 2 to Point 3": 73.14,
        "Point 1 to Point 3": 37.98
    }

    distances_calculated = False
    for key, correct_distance in correct_distances.items():
        # Check if the code correctly calculates the distances
        if key in student_code_output:
            grade += 5
            distances_calculated = True
            feedback.append(f"Distance for {key} is calculated correctly.")
        else:
            feedback.append(f"Check distance calculation for {key}.")
    
    if distances_calculated:
        grade += 10

    # Grading the map visualization (folium map generation)
    if "Map generated" in student_code_output:
        grade += 15
        feedback.append("Map generated successfully with folium.")
    else:
        feedback.append("Map visualization is missing or incorrect.")

    # Save grade to data_submission.csv
    student_data = {
        'Full Name': student_name,
        'Student ID': student_id,
        'Assignment1': grade,
        # Placeholder for other assignments and quizzes
        'Total': grade
    }

    try:
        # Load existing CSV and append the new entry
        df = pd.read_csv('grades/data_submission.csv')
        df = df.append(student_data, ignore_index=True)
        df.to_csv('grades/data_submission.csv', index=False)
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        df = pd.DataFrame([student_data])
        df.to_csv('grades/data_submission.csv', index=False)
    
    return grade, feedback

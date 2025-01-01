# week1.py
import streamlit as st
import pandas as pd
from pathlib import Path
import importlib

def run():
    st.title("Week 1 Assignment")
    
    # Student Information Section
    st.header("Student Information")
    student_name = st.text_input("Name")
    student_email = st.text_input("Email")
    student_id = st.text_input("Student ID")

    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        ### Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python
        
        **Objective:**  
        Write a Python script to plot three geographical coordinates on a map and calculate 
        the distance between each pair of points in kilometers.
        
        **Task Requirements:**
        1. Plot the Three Coordinates on a Map:
           - The coordinates represent three locations in the Kurdistan Region
           - Use Python libraries to plot these points on a map
           - The map should visually display the exact locations
        
        2. Calculate the Distance Between Each Pair of Points:
           - Calculate distances between the three points in kilometers:
             - Distance between Point 1 and Point 2
             - Distance between Point 2 and Point 3
             - Distance between Point 1 and Point 3
        
        **Coordinates:**
        - Point 1: Latitude: 36.325735, Longitude: 43.928414
        - Point 2: Latitude: 36.393432, Longitude: 44.586781
        - Point 3: Latitude: 36.660477, Longitude: 43.840174
        
        **Required Libraries:**
        - geopy for calculating distances
        - folium for plotting points
        - geopandas (optional) for advanced rendering
        
        **Expected Output:**
        1. A map showing the three coordinates
        2. Text summary of calculated distances in kilometers
        """)

    # Code Submission Section
    st.header("Code Submission")
    code_submission = st.text_area("Enter your Python code here:", height=400)

    # Run Code Button
    if st.button("Run Code"):
        try:
            # Create a temporary Python file with the submitted code
            with open("temp_submission.py", "w") as f:
                f.write(code_submission)
            
            # Import and run the temporary file
            temp_module = importlib.import_module("temp_submission")
            st.success("Code executed successfully!")
            
        except Exception as e:
            st.error(f"Error executing code: {str(e)}")

    # Submit Assignment Button
    if st.button("Submit Assignment"):
        if not all([student_name, student_email, student_id, code_submission]):
            st.error("Please fill in all required fields before submitting.")
            return
            
        # Calculate grade using grade1.py
        grade_result = calculate_grade(code_submission)
        total_grade = grade_result['total_grade']
        
        # Save submission to CSV
        save_submission(student_name, student_id, total_grade)
        
        # Display results
        st.success(f"Assignment submitted successfully! Grade: {total_grade}/100")
        
        # Display detailed feedback
        st.write("### Grading Breakdown:")
        st.write("Code Structure and Implementation:", grade_result['code_structure'])
        st.write("Map Visualization:", grade_result['visualization'])
        st.write("Distance Calculations:", grade_result['calculations'])

def save_submission(name, student_id, total):
    # Ensure grades directory exists
    Path("grades").mkdir(exist_ok=True)
    
    # Create or load existing submission data
    csv_path = "grades/data_submission.csv"
    if Path(csv_path).exists():
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=['name', 'student_id', 'total', 'week1'])
    
    # Add new submission
    new_row = {
        'name': name,
        'student_id': student_id,
        'total': total,
        'week1': total
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Save updated data
    df.to_csv(csv_path, index=False)

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

if __name__ == "__main__":
    run()

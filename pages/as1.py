# pages/as1.py
import streamlit as st
import sys
import io
import contextlib
import pandas as pd
import os
import ast
import re

def grade_assignment(code):
    total_points = 0
    feedback = []
    
    # Code Structure and Implementation (30 points)
    structure_points = grade_structure(code)
    total_points += structure_points
    feedback.append(f"Code Structure: {structure_points}/30")
    
    # Map Visualization (40 points)
    vis_points = grade_visualization(code)
    total_points += vis_points
    feedback.append(f"Visualization: {vis_points}/40")
    
    # Distance Calculations (30 points)
    calc_points = grade_calculations(code)
    total_points += calc_points
    feedback.append(f"Calculations: {calc_points}/30")
    
    return total_points, "\n".join(feedback)

def grade_structure(code):
    points = 0
    if all(lib in code for lib in ['geopy', 'folium']):
        points += 5
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
    try:
        compile(code, '<string>', 'exec')
        points += 10
    except:
        pass
    if len(code.split('\n')) < 50 and 'def' in code:
        points += 10
    elif 'def' in code:
        points += 5
    return min(30, points)

def grade_visualization(code):
    points = 0
    if 'folium.Map' in code:
        points += 15
    if 'folium.Marker' in code and code.count('Marker') >= 3:
        points += 15
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
    if 'geodesic' in code:
        points += 10
    for distance in expected_distances.values():
        if str(round(distance, 2)) in code:
            points += 6.67
    return min(30, points)

def save_grade(full_name, student_id, grade):
    csv_path = "grades/data_submission.csv"
    os.makedirs("grades", exist_ok=True)
    
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=[
            "full_name", "student_id"] + 
            [f"assignment{i}" for i in range(1, 16)] +
            [f"quiz{i}" for i in range(1, 11)] +
            ["total"])
    else:
        df = pd.read_csv(csv_path)
    
    student_row = df[df['student_id'] == student_id].index
    if len(student_row) > 0:
        df.loc[student_row, 'assignment1'] = grade
        assignments = df.loc[student_row, [f'assignment{i}' for i in range(1, 16)]].fillna(0)
        quizzes = df.loc[student_row, [f'quiz{i}' for i in range(1, 11)]].fillna(0)
        df.loc[student_row, 'total'] = assignments.mean() * 0.7 + quizzes.mean() * 0.3
    else:
        new_row = pd.DataFrame({
            'full_name': [full_name],
            'student_id': [student_id],
            'assignment1': [grade]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    
    df.to_csv(csv_path, index=False)

def main():
    st.title("Week 1 Assignment")
    
    with st.form("student_info"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", key="name")
            email = st.text_input("Email", key="email")
        with col2:
            student_id = st.text_input("Student ID", key="id")

        with st.expander("Assignment Details", expanded=True):
            st.markdown("""
            ### Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python
            
            **Objective:** In this assignment, you will write a Python script to plot three geographical coordinates 
            on a map and calculate the distance between each pair of points in kilometers.
            
            **Task Requirements:**
            1. Plot the Three Coordinates on a Map:
               - The coordinates represent three locations in the Kurdistan Region
               - Use Python libraries to plot these points on a map
               - The map should visually display the exact locations
            
            2. Calculate the Distance Between Each Pair of Points:
               - Calculate distances in kilometers between:
                 - Point 1 and Point 2
                 - Point 2 and Point 3
                 - Point 1 and Point 3
            
            **Coordinates:**
            - Point 1: 36.325735, 43.928414
            - Point 2: 36.393432, 44.586781
            - Point 3: 36.660477, 43.840174
            
            **Required Libraries:**
            ```python
            from geopy.distance import geodesic
            import folium
            ```
            """)

        st.subheader("Code Submission")
        code = st.text_area("Paste your code here:", height=300, key="code")
        
        submitted = st.form_submit_button("Submit Assignment")
        
    if st.button("Run Code", key="run"):
        if code:
            try:
                # Create a safe globals dictionary with necessary modules
                safe_globals = {
                    'folium': __import__('folium'),
                    'geopy': __import__('geopy'),
                    'geodesic': __import__('geopy.distance').distance.geodesic,
                }
                
                # Capture stdout
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    exec(code, safe_globals)
                
                st.write("Output:")
                st.write(stdout.getvalue())
                
                # Display map if it was created
                if 'map' in safe_globals:
                    map_html = safe_globals['map']._repr_html_()
                    st.components.v1.html(map_html, height=500)
                
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")

    if submitted:
        if not all([full_name, email, student_id, code]):
            st.error("Please fill in all fields")
            return

        grade, feedback = grade_assignment(code)
        
        st.success(f"Total Grade: {grade}/100")
        st.write("Feedback:")
        for line in feedback.split('\n'):
            st.write(line)
        
        save_grade(full_name, student_id, grade)
        st.success("Grade saved successfully!")

if __name__ == "__main__":
    main()

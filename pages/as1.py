# pages/as1.py
import streamlit as st
import sys
import io
import contextlib
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

def main():
    st.title("Week 1 Assignment")
    
    with st.form("student_info"):
        col1, col2, col3 = st.columns(3)
        with col1:
            full_name = st.text_input("Full Name")
        with col2:
            email = st.text_input("Email")
        with col3:
            student_id = st.text_input("Student ID")
        
        with st.expander("Assignment Details", expanded=True):
            st.markdown("""
            **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**
            
            **Objective:** Create a Python script to plot geographical coordinates and calculate distances.
            
            **Coordinates:**
            - Point 1: 36.325735, 43.928414
            - Point 2: 36.393432, 44.586781
            - Point 3: 36.660477, 43.840174
            
            **Required Libraries:**
            ```python
            import folium
            from geopy.distance import geodesic
            ```
            """)

        st.subheader("Code Submission")
        code = st.text_area("Paste your code here:", height=300)
        submit_button = st.form_submit_button("Submit Assignment")

    if st.button("Run Code"):
        if code:
            try:
                # Create a string buffer to capture print outputs
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    # Execute the code in a safe environment
                    local_dict = {}
                    exec(code, {"folium": folium, "geodesic": geodesic, "st": st, 
                               "st_folium": st_folium}, local_dict)
                
                # Display any print outputs
                output = stdout.getvalue()
                if output:
                    st.text("Program Output:")
                    st.code(output)
                    
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")

    if submit_button:
        if not all([full_name, email, student_id, code]):
            st.error("Please fill in all fields")
            return

        try:
            # Grade submission
            points = grade_submission(code)
            
            # Save grade
            save_grade(full_name, student_id, points)
            
            st.success(f"Assignment submitted! Grade: {points}/100")
        except Exception as e:
            st.error(f"Error processing submission: {str(e)}")

def grade_submission(code):
    points = 0
    
    # Check for required libraries
    if "import folium" in code and "geodesic" in code:
        points += 10
        
    # Check for coordinates
    coordinates = [
        "36.325735, 43.928414",
        "36.393432, 44.586781",
        "36.660477, 43.840174"
    ]
    for coord in coordinates:
        if coord in code:
            points += 5
            
    # Check for map creation and markers
    if "folium.Map" in code:
        points += 15
    if "Marker" in code:
        points += 15
        
    # Check for distance calculations
    expected_distances = ["59.57", "73.14", "37.98"]
    for dist in expected_distances:
        if dist in code:
            points += 10
            
    # Code structure and efficiency
    if "def" in code and len(code.split('\n')) < 50:
        points += 10
        
    return points

def save_grade(full_name, student_id, grade):
    # Create grades directory if it doesn't exist
    os.makedirs('grades', exist_ok=True)
    
    file_path = 'grades/data_submission.csv'
    
    # Create or load the DataFrame
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        columns = ['full_name', 'student_id'] + \
                 [f'assignment{i}' for i in range(1, 16)] + \
                 [f'quiz{i}' for i in range(1, 11)] + \
                 ['total']
        df = pd.DataFrame(columns=columns)
    
    # Update or add new row
    if student_id in df['student_id'].values:
        df.loc[df['student_id'] == student_id, 'assignment1'] = grade
    else:
        new_row = pd.DataFrame({
            'full_name': [full_name],
            'student_id': [student_id],
            'assignment1': [grade]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    
    # Calculate total
    assignment_cols = [f'assignment{i}' for i in range(1, 16)]
    quiz_cols = [f'quiz{i}' for i in range(1, 11)]
    
    df['total'] = df[assignment_cols].fillna(0).mean(axis=1) * 0.7 + \
                 df[quiz_cols].fillna(0).mean(axis=1) * 0.3
    
    # Save to CSV
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    main()

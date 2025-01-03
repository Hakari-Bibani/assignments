import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from grades.grade1 import grade_assignment

def render_assignment_page():
    st.title("Week 1 Assignment - Mapping Coordinates and Calculating Distances")
    
    # Student Information Form
    with st.form("student_info"):
        st.write("### Student Information")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        student_id = st.text_input("Student ID")
        
        # Assignment Details in Accordion
        with st.expander("Assignment Details", expanded=True):
            st.markdown("""
            **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**
            
            **Objective:** Write a Python script to plot three geographical coordinates on a map and calculate 
            the distance between each pair of points in kilometers.
            
            **Task Requirements:**
            1. **Plot the Three Coordinates on a Map:**
                - Plot three locations in the Kurdistan Region
                - Use Python libraries to create an interactive map
                - Display exact locations of the coordinates
            
            2. **Calculate the Distance Between Each Pair of Points:**
                - Calculate distances in **kilometers** between:
                    - Point 1 and Point 2
                    - Point 2 and Point 3
                    - Point 1 and Point 3
            
            **Coordinates:**
            - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
            - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
            - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
            
            **Required Libraries:**
            - geopy: For distance calculations
            - folium: For interactive mapping
            - geopandas (optional): For advanced map rendering
            """)
        
        # Code Input Area
        st.write("### Code Submission")
        code_submission = st.text_area("Enter your Python code here", height=300)
        
        submitted = st.form_submit_button("Submit Assignment")
        
        if submitted:
            if not all([full_name, email, student_id, code_submission]):
                st.error("Please fill in all required fields")
                return
            
            try:
                # Execute the code
                st.write("### Output:")
                
                # Create a temporary Python file
                temp_file = "temp_submission.py"
                with open(temp_file, "w") as f:
                    f.write(code_submission)
                
                # Execute the code and capture output
                try:
                    exec(code_submission, globals())
                    
                    # Grade the submission
                    grade, feedback = grade_assignment(code_submission)
                    
                    # Display grade and feedback
                    st.write(f"### Grade: {grade}/100")
                    st.write("### Feedback:")
                    st.write(feedback)
                    
                    # Save to CSV
                    csv_path = "grades/data_submission.csv"
                    
                    # Create or load existing CSV
                    if os.path.exists(csv_path):
                        df = pd.read_csv(csv_path)
                    else:
                        columns = ['Full name', 'student ID'] + [f'assignment{i}' for i in range(1, 16)] + \
                                [f'quiz{i}' for i in range(1, 11)] + ['total']
                        df = pd.DataFrame(columns=columns)
                    
                    # Update or add new row
                    student_row = df[df['student ID'] == student_id]
                    if len(student_row) > 0:
                        df.loc[df['student ID'] == student_id, 'assignment1'] = grade
                    else:
                        new_row = pd.DataFrame({
                            'Full name': [full_name],
                            'student ID': [student_id],
                            'assignment1': [grade]
                        })
                        df = pd.concat([df, new_row], ignore_index=True)
                    
                    # Calculate total
                    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                    df['total'] = df[numeric_columns].sum(axis=1)
                    
                    # Save to CSV
                    df.to_csv(csv_path, index=False)
                    
                    st.success("Assignment submitted successfully!")
                    
                except Exception as e:
                    st.error(f"Error executing code: {str(e)}")
                
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        
            except Exception as e:
                st.error(f"Error processing submission: {str(e)}")

if __name__ == "__main__":
    render_assignment_page()

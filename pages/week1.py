import streamlit as st
import pandas as pd
import sys
import os
from grade1 import grade_assignment
import io
from contextlib import redirect_stdout

def run_student_code(code_string):
    # Capture output
    output = io.StringIO()
    with redirect_stdout(output):
        try:
            exec(code_string)
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)

st.title("Week 1 Assignment")
st.markdown("### Mapping Coordinates and Calculating Distances in Python")

# Student Information
st.subheader("Student Information")
col1, col2, col3 = st.columns(3)
with col1:
    student_name = st.text_input("Name")
with col2:
    student_email = st.text_input("Email")
with col3:
    student_id = st.text_input("Student ID")

# Assignment Details in Accordion
with st.expander("📝 Assignment Details", expanded=True):
    st.markdown("""
    **Objective:** Write a Python script to plot three geographical coordinates on a map and calculate 
    the distance between each pair of points in kilometers.
    
    **Task Requirements:**
    1. **Plot the Three Coordinates on a Map:**
        - Plot coordinates from Kurdistan Region
        - Use Python libraries for visualization
        - Display exact locations on the map
    
    2. **Calculate the Distance Between Each Pair of Points:**
        - Calculate distances in **kilometers**:
            - Distance between Point 1 and Point 2
            - Distance between Point 2 and Point 3
            - Distance between Point 1 and Point 3
    
    **Coordinates:**
    - Point 1: Latitude: 36.325735, Longitude: 43.928414
    - Point 2: Latitude: 36.393432, Longitude: 44.586781
    - Point 3: Latitude: 36.660477, Longitude: 43.840174
    
    **Required Libraries:**
    - geopy (for distance calculations)
    - folium (for interactive mapping)
    - geopandas (optional)
    """)

# Code Submission
st.subheader("Code Submission")
code_submission = st.text_area("Enter your Python code here:", height=300)

# Run Code Button
if st.button("Run Code"):
    if code_submission.strip():
        st.markdown("### Output:")
        output, error = run_student_code(code_submission)
        if error:
            st.error(f"Error in code execution:\n{error}")
        else:
            st.success("Code executed successfully!")
            st.text(output)
    else:
        st.warning("Please enter code before running.")

# Submit Assignment Button
if st.button("Submit Assignment"):
    if not all([student_name, student_email, student_id, code_submission]):
        st.error("Please fill in all fields before submitting.")
    else:
        # Calculate grade
        grade, feedback = grade_assignment(code_submission)
        
        # Prepare data for CSV
        submission_data = {
            'Name': [student_name],
            'Email': [student_email],
            'Student ID': [student_id],
            'Week 1': [grade],
            'Total': [grade]  # For week 1, total is same as week 1 grade
        }
        
        # Create or update CSV file
        csv_path = 'grades/data_submission.csv'
        try:
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                new_df = pd.DataFrame(submission_data)
                # Update if student exists, append if new
                df = pd.concat([df[df['Student ID'] != student_id], new_df]).reset_index(drop=True)
            else:
                os.makedirs(os.path.dirname(csv_path), exist_ok=True)
                df = pd.DataFrame(submission_data)
            
            df.to_csv(csv_path, index=False)
            
            # Display results
            st.success(f"Assignment submitted successfully! Your grade: {grade}/100")
            st.markdown("### Feedback:")
            for category, notes in feedback.items():
                st.markdown(f"**{category}:**")
                for note in notes:
                    st.markdown(f"- {note}")
                    
        except Exception as e:
            st.error(f"Error saving submission: {str(e)}")

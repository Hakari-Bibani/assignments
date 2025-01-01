import streamlit as st
import pandas as pd
import os
import sys
import io
from IPython.display import display
import folium
from geopy.distance import geodesic
import importlib

st.title("Week 1: Mapping Coordinates and Calculating Distances")

# Student Information Section
st.header("Student Information")
name = st.text_input("Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID")

# Assignment Details Section
with st.expander("Assignment Details", expanded=True):
    st.markdown("""
    **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**
    
    **Objective:** In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.
    
    **Task Requirements:**
    1. **Plot the Three Coordinates on a Map:**
        - The coordinates represent three locations in the Kurdistan Region
        - Use Python libraries to plot these points on a map
        - The map should visually display the exact locations of the coordinates
        
    2. **Calculate the Distance Between Each Pair of Points:**
        - Calculate the distances between the three points in **kilometers**
        - Specifically, calculate:
            - The distance between **Point 1** and **Point 2**
            - The distance between **Point 2** and **Point 3**
            - The distance between **Point 1** and **Point 3**
    
    **Coordinates:**
    - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
    - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
    - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
    
    **Required Libraries:**
    - **geopy** for calculating distance between coordinates
    - **folium** for plotting points on an interactive map
    - **geopandas** (optional) for advanced map rendering
    """)

# Code Submission Section
st.header("Code Submission")
code = st.text_area("Enter your Python code here", height=300)

# Run Code Button
if st.button("Run Code"):
    if code.strip():
        try:
            # Capture stdout to display print statements
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()

            # Execute the code
            exec(code)

            # Restore stdout and get the output
            sys.stdout = old_stdout
            output = redirected_output.getvalue()

            # Display the output
            if output:
                st.text("Output:")
                st.text(output)

            # Look for Folium map object in local variables
            local_vars = locals()
            for var in local_vars:
                if isinstance(local_vars[var], folium.Map):
                    st_folium(local_vars[var])

        except Exception as e:
            st.error(f"Error executing code: {str(e)}")
    else:
        st.warning("Please enter some code before running.")

# Submit Assignment Button
if st.button("Submit Assignment"):
    if not all([name, email, student_id, code]):
        st.error("Please fill in all fields before submitting.")
    else:
        try:
            # Import grading function
            grade_module = importlib.import_module('grade1')
            grade_result = grade_module.grade_assignment(code)
            
            # Display grade
            st.success(f"Total Grade: {grade_result}/100")
            
            # Save to CSV
            df = pd.DataFrame({
                'name': [name],
                'student_id': [student_id],
                'total': [0],  # Will be updated with total from all weeks
                'week1': [grade_result]
            })
            
            # Create grades directory if it doesn't exist
            os.makedirs('grades', exist_ok=True)
            
            # Load existing data or create new file
            csv_path = 'grades/data_submission.csv'
            if os.path.exists(csv_path):
                existing_df = pd.read_csv(csv_path)
                # Update if student exists, append if new
                if student_id in existing_df['student_id'].values:
                    existing_df.loc[existing_df['student_id'] == student_id, 'week1'] = grade_result
                    existing_df.to_csv(csv_path, index=False)
                else:
                    df.to_csv(csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_path, index=False)
                
            st.success("Assignment submitted successfully!")
            
        except Exception as e:
            st.error(f"Error during submission: {str(e)}")

import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import folium_static
import os
import sys

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from utils.grading import grade_assignment

def run_student_code(code_string):
    try:
        # Create a local namespace
        local_namespace = {}
        # Execute the student's code
        exec(code_string, globals(), local_namespace)
        
        # Check if required variables exist
        required_vars = ['distances', 'map_obj']
        for var in required_vars:
            if var not in local_namespace:
                return None, f"Error: Missing required variable '{var}'"
        
        return local_namespace['distances'], local_namespace['map_obj']
    except Exception as e:
        return None, f"Error: {str(e)}"

def app():
    st.title("Assignment 1: Mapping Coordinates and Calculating Distances")
    
    # Student Information Form
    with st.form("student_info"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        student_id = st.text_input("Student ID")
        next_button = st.form_submit_button("Next")

    if next_button and full_name and email and student_id:
        # Assignment Details Accordion
        with st.expander("Assignment Details", expanded=True):
            st.markdown("""
            ### Objective:
            Write a Python script to plot three geographical coordinates on a map and calculate 
            the distance between each pair of points in kilometers.

            ### Coordinates:
            - Point 1: (36.325735, 43.928414)
            - Point 2: (36.393432, 44.586781)
            - Point 3: (36.660477, 43.840174)

            ### Required Libraries:
            - folium
            - geopy
            """)

        # Code Input
        code = st.text_area("Enter your Python code here:", height=300)

        # Run Code Button
        if st.button("Run Code"):
            if code:
                distances, map_obj = run_student_code(code)
                if isinstance(map_obj, folium.Map):
                    st.write("Map Output:")
                    folium_static(map_obj)
                    
                if distances:
                    st.write("Distance Report:")
                    st.write(distances)
                else:
                    st.error("Error in distance calculations")
            else:
                st.warning("Please enter code before running")

        # Submit Button
        if st.button("Submit"):
            if code:
                # Grade the submission
                grade = grade_assignment(code)
                
                # Save submission to CSV
                submission_data = {
                    'Full Name': [full_name],
                    'Student ID': [student_id],
                    'Email': [email],
                    'Assignment 1': [grade],
                    'Total': [grade]
                }
                df = pd.DataFrame(submission_data)
                
                # Create data directory if it doesn't exist
                os.makedirs('data', exist_ok=True)
                
                try:
                    # Try to read existing CSV file
                    existing_df = pd.read_csv('data/submissions.csv')
                    # Append new submission
                    updated_df = pd.concat([existing_df, df], ignore_index=True)
                except FileNotFoundError:
                    # If file doesn't exist, create new one
                    updated_df = df
                
                # Save to CSV
                updated_df.to_csv('data/submissions.csv', index=False)
                
                st.success(f"Assignment submitted successfully! Grade: {grade}/100")
            else:
                st.warning("Please enter code before submitting")

if __name__ == "__main__":
    app()

import streamlit as st
import pandas as pd
import folium
from folium import plugins
from geopy.distance import geodesic
import sys
import io
from streamlit_folium import folium_static
from grade1 import grade_assignment
import os

def save_submission(name, email, student_id, grade):
    # Create grades directory if it doesn't exist
    os.makedirs('grades', exist_ok=True)
    
    # Prepare the data
    data = {
        'Name': [name],
        'Email': [email],
        'Student ID': [student_id],
        'Total': [grade],
        'Week1': [grade]
    }
    
    file_path = 'grades/data_submission.csv'
    
    # Check if file exists
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Update or append
        mask = df['Student ID'] == student_id
        if mask.any():
            df.loc[mask, ['Week1', 'Total']] = grade
        else:
            df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    else:
        df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(file_path, index=False)

def main():
    st.title("Week 1 Assignment")
    
    # Student Information
    st.header("Student Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    
    # Assignment Details
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        ### Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python
        
        **Objective:**
        Write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.
        
        **Task Requirements:**
        1. Plot the Three Coordinates on a Map:
           - The coordinates represent three locations in the Kurdistan Region.
           - Use Python libraries to plot these points on a map.
           - The map should visually display the exact locations of the coordinates.
        
        2. Calculate the Distance Between Each Pair of Points:
           - Calculate the distances between the three points in kilometers.
           - Specifically, calculate:
             - The distance between Point 1 and Point 2
             - The distance between Point 2 and Point 3
             - The distance between Point 1 and Point 3
        
        **Coordinates:**
        - Point 1: Latitude: 36.325735, Longitude: 43.928414
        - Point 2: Latitude: 36.393432, Longitude: 44.586781
        - Point 3: Latitude: 36.660477, Longitude: 43.840174
        
        **Required Libraries:**
        - geopy for calculating the distance between two coordinates
        - folium for plotting the points on an interactive map
        - geopandas (optional) for advanced map rendering
        """)
    
    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Enter your Python code here", height=300)
    
    # Run Code Button
    if st.button("Run Code"):
        if code.strip():
            # Capture output
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            
            try:
                # Execute code
                exec(code)
                
                # Restore stdout
                sys.stdout = old_stdout
                output = redirected_output.getvalue()
                
                # Display output
                st.text("Output:")
                st.text(output)
                
            except Exception as e:
                sys.stdout = old_stdout
                st.error(f"Error executing code: {str(e)}")
    
    # Submit Assignment Button
    if st.button("Submit Assignment"):
        if not all([name, email, student_id, code]):
            st.error("Please fill in all required fields")
            return
            
        # Grade the submission
        grade = grade_assignment(code)
        
        # Save submission
        save_submission(name, email, student_id, grade)
        
        # Display results
        st.success(f"Assignment submitted successfully!")
        st.info(f"Your grade: {grade}/100")

if __name__ == "__main__":
    main()

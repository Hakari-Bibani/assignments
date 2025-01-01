import streamlit as st
import pandas as pd
import os
from grade1 import grade_assignment
import sys
import io
from contextlib import redirect_stdout

def main():
    st.title("Week 1 Assignment")
    
    # Student Information Section
    st.header("Student Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    
    # Assignment Details Section
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        ## Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python
        
        ### Objective:
        In this assignment, you will write a Python script to plot three geographical coordinates 
        on a map and calculate the distance between each pair of points in kilometers.
        
        ### Task Requirements:
        1. **Plot the Three Coordinates on a Map:**
           - The coordinates represent three locations in the Kurdistan Region
           - Use Python libraries to plot these points on a map
           - The map should visually display the exact locations of the coordinates
        
        2. **Calculate the Distance Between Each Pair of Points:**
           - Calculate the distances between the three points in **kilometers**
           - Specifically calculate:
             - The distance between **Point 1** and **Point 2**
             - The distance between **Point 2** and **Point 3**
             - The distance between **Point 1** and **Point 3**
        
        ### Coordinates:
        - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
        - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
        - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
        
        ### Python Libraries You Will Use:
        - **geopy** for calculating the distance between two coordinates
        - **folium** for plotting the points on an interactive map
        - **geopandas** (optional) for advanced map rendering
        """)
    
    # Code Submission Section
    st.header("Code Submission")
    code = st.text_area("Enter your code here:", height=300)
    
    # Run Code Button
    if st.button("Run Code"):
        if code.strip():
            try:
                # Capture output
                output = io.StringIO()
                with redirect_stdout(output):
                    exec(code)
                st.write("Output:")
                st.write(output.getvalue())
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
        else:
            st.warning("Please enter code before running.")
    
    # Submit Assignment Button
    if st.button("Submit Assignment"):
        if not all([name, email, student_id, code]):
            st.error("Please fill in all fields before submitting.")
            return
        
        # Grade the assignment
        total_grade = grade_assignment(code)
        
        # Save to CSV
        data = {
            'Name': [name],
            'Email': [email],
            'Student_ID': [student_id],
            'Week1': [total_grade],
            'Total': [total_grade]  # For week 1, total is same as week1 grade
        }
        
        df = pd.DataFrame(data)
        
        # Create grades directory if it doesn't exist
        os.makedirs('grades', exist_ok=True)
        
        # Check if file exists and append/create accordingly
        csv_path = 'grades/data_submission.csv'
        if os.path.exists(csv_path):
            existing_df = pd.read_csv(csv_path)
            # Update if student exists, append if new
            if student_id in existing_df['Student_ID'].values:
                existing_df.loc[existing_df['Student_ID'] == student_id, 'Week1'] = total_grade
                existing_df.loc[existing_df['Student_ID'] == student_id, 'Total'] = total_grade
                existing_df.to_csv(csv_path, index=False)
            else:
                df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)
        
        st.success(f"Assignment submitted successfully! Your grade: {total_grade}/100")

if __name__ == "__main__":
    main()

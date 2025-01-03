import streamlit as st
import pandas as pd
import sys
import io
from grade1 import grade_assignment
import json
import os

def main():
    st.title("Week 1 Assignment - Mapping Coordinates and Calculating Distances")
    
    # Student Information
    st.header("Student Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        full_name = st.text_input("Full Name")
    with col2:
        email = st.text_input("Email")
    with col3:
        student_id = st.text_input("Student ID")

    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        **Objective:** Write a Python script to plot three geographical coordinates on a map and calculate 
        the distance between each pair of points in kilometers.
        
        **Task Requirements:**
        1. **Plot the Three Coordinates on a Map:**
           - Plot three locations in the Kurdistan Region
           - Use Python libraries to display points on a map
           
        2. **Calculate the Distance Between Each Pair of Points:**
           - Calculate distances in **kilometers**:
             - Distance between Point 1 and Point 2
             - Distance between Point 2 and Point 3
             - Distance between Point 1 and Point 3
        
        **Coordinates:**
        - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
        - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
        - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
        
        **Required Libraries:**
        ```python
        import folium
        from geopy.distance import geodesic
        ```
        """)

    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Paste your code here:", height=300)
    
    # Buttons for Run and Submit
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("Run Code")
    with col2:
        submit_button = st.button("Submit Assignment")

    # Run Code Logic
    if run_button and code:
        try:
            # Capture output
            old_stdout = sys.stdout
            redirected_output = io.StringIO()
            sys.stdout = redirected_output

            # Execute the code
            exec(code, globals())
            
            # Restore stdout
            sys.stdout = old_stdout
            
            # Display output
            st.subheader("Output:")
            output = redirected_output.getvalue()
            if output:
                st.text(output)

            # Display map if 'm' variable exists in globals
            if 'm' in globals() and isinstance(globals()['m'], folium.Map):
                folium_map = globals()['m']
                folium_map.save("temp_map.html")
                with open("temp_map.html", "r") as f:
                    st.components.v1.html(f.read(), height=500)
                os.remove("temp_map.html")

        except Exception as e:
            st.error(f"Error executing code: {str(e)}")

    # Submit Logic
    if submit_button:
        if not all([full_name, email, student_id, code]):
            st.error("Please fill in all fields before submitting.")
            return

        # Grade the submission
        grade, feedback = grade_assignment(code)
        
        # Display results
        st.success(f"Assignment submitted successfully! Grade: {grade}/100")
        st.write("Feedback:", feedback)
        
        # Save grade to CSV
        try:
            df = pd.read_csv('grades/data_submission.csv')
        except FileNotFoundError:
            # Create new DataFrame if file doesn't exist
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
        df.to_csv('grades/data_submission.csv', index=False)

if __name__ == "__main__":
    main()

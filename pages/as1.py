import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
import sys
from io import StringIO
import contextlib

def run_assignment():
    st.title("Week 1 Assignment - Mapping Coordinates")
    
    # Student Information
    with st.form("student_info"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        student_id = st.text_input("Student ID")
        
        # Assignment Details in Accordion
        with st.expander("Assignment Details", expanded=True):
            st.markdown("""
            **Objective:** Plot geographical coordinates and calculate distances in Python
            
            **Coordinates:**
            - Point 1: 36.325735, 43.928414
            - Point 2: 36.393432, 44.586781
            - Point 3: 36.660477, 43.840174
            
            **Required Libraries:**
            - geopy for distance calculations
            - folium for mapping
            - geopandas (optional)
            """)
        
        # Code Input
        code = st.text_area("Paste your code here:", height=300)
        
        submitted = st.form_submit_button("Submit Assignment")

    if st.button("Run Code"):
        if code:
            try:
                # Create string buffer to capture print outputs
                output = StringIO()
                with contextlib.redirect_stdout(output):
                    # Create a local namespace for execution
                    local_dict = {}
                    # Execute the code
                    exec(code, globals(), local_dict)
                
                # Get the output
                output_str = output.getvalue()
                
                # Display the distance calculations
                if output_str:
                    st.subheader("Distance Calculations:")
                    st.text(output_str)
                
                # Display the map if it was created
                if 'm' in local_dict and isinstance(local_dict['m'], folium.Map):
                    st.subheader("Map Visualization:")
                    st_folium(local_dict['m'], width=700, height=500)
                
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
    
    if submitted and full_name and email and student_id and code:
        # Calculate grade
        from grade1 import grade_assignment
        grade = grade_assignment(code)
        
        # Create grades directory if it doesn't exist
        os.makedirs('grades', exist_ok=True)
        
        # Create or load CSV file
        csv_path = "grades/data_submission.csv"
        if not os.path.exists(csv_path):
            df = pd.DataFrame(columns=['full_name', 'student_id', 'email'] + 
                            [f'assignment{i}' for i in range(1, 16)] +
                            [f'quiz{i}' for i in range(1, 11)] +
                            ['total'])
        else:
            df = pd.read_csv(csv_path)
        
        # Check if student exists
        mask = df['student_id'] == student_id
        if mask.any():
            df.loc[mask, 'assignment1'] = grade
        else:
            new_row = pd.DataFrame([{
                'full_name': full_name,
                'student_id': student_id,
                'email': email,
                'assignment1': grade
            }])
            df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_csv(csv_path, index=False)
        st.success(f"Assignment submitted! Grade: {grade}/100")
    elif submitted:
        st.warning("Please fill in all required fields")

if __name__ == "__main__":
    run_assignment()

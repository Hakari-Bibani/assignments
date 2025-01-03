import streamlit as st
import pandas as pd
import os

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
                # Execute code and capture output
                exec(code, globals())
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
    
    if submitted and full_name and email and student_id and code:
        # Calculate grade
        from grade1 import grade_assignment
        grade = grade_assignment(code)
        
        # Save to CSV
        df = pd.read_csv("grades/data_submission.csv")
        
        # Check if student exists
        mask = df['student_id'] == student_id
        if mask.any():
            df.loc[mask, 'assignment1'] = grade
        else:
            new_row = pd.DataFrame([{
                'full_name': full_name,
                'student_id': student_id,
                'assignment1': grade,
            }])
            df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_csv("grades/data_submission.csv", index=False)
        st.success(f"Assignment submitted! Grade: {grade}/100")
    elif submitted:
        st.warning("Please fill in all required fields")

if __name__ == "__main__":
    run_assignment()

# as1.py
import streamlit as st
import pandas as pd
import os
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
                    # Execute the code
                    exec(code)
                
                # Display the output
                st.text(output.getvalue())
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
    
    if submitted and full_name and email and student_id and code:
        try:
            # Calculate grade
            from grade1 import grade_assignment
            grade = grade_assignment(code)
            
            # Create grades directory if it doesn't exist
            os.makedirs('grades', exist_ok=True)
            
            # Create or load CSV file
            csv_path = "grades/data_submission.csv"
            if not os.path.exists(csv_path):
                columns = ['full_name', 'student_id', 'email']
                for i in range(1, 16):
                    columns.append(f'assignment{i}')
                for i in range(1, 11):
                    columns.append(f'quiz{i}')
                columns.append('total')
                df = pd.DataFrame(columns=columns)
            else:
                df = pd.read_csv(csv_path)
            
            # Update or add new student record
            new_data = {
                'full_name': full_name,
                'student_id': student_id,
                'email': email,
                'assignment1': grade
            }
            
            if student_id in df['student_id'].values:
                df.loc[df['student_id'] == student_id, 'assignment1'] = grade
            else:
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            
            df.to_csv(csv_path, index=False)
            st.success(f"Assignment submitted! Grade: {grade}/100")
        except Exception as e:
            st.error(f"Error during submission: {str(e)}")
    elif submitted:
        st.warning("Please fill in all required fields")

if __name__ == "__main__":
    run_assignment()

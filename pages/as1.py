import streamlit as st
import sys
import io
import contextlib
import pandas as pd
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grades.grade1 import grade_assignment

def main():
    st.title("Week 1 Assignment")
    
    # Student Information
    with st.form("student_info"):
        st.subheader("Student Information")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        student_id = st.text_input("Student ID")
        
        # Assignment Details in Accordion
        with st.expander("Assignment Details", expanded=True):
            st.markdown("""
            **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**
            
            **Objective:** Create a Python script to plot geographical coordinates and calculate distances.
            
            **Coordinates:**
            - Point 1: 36.325735, 43.928414
            - Point 2: 36.393432, 44.586781
            - Point 3: 36.660477, 43.840174
            
            **Required Libraries:**
            - geopy
            - folium
            - geopandas (optional)
            """)

        # Code Submission
        st.subheader("Code Submission")
        code = st.text_area("Paste your code here:", height=300)
        
        # Submit button for the form
        submitted = st.form_submit_button("Submit Assignment")

    # Run Code button (outside the form)
    if st.button("Run Code"):
        if code:
            try:
                # Capture stdout
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    exec(code)
                st.write("Output:")
                st.write(stdout.getvalue())
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")

    # Handle submission
    if submitted:
        if not all([full_name, email, student_id, code]):
            st.error("Please fill in all fields")
            return

        # Grade the submission
        grade, feedback = grade_assignment(code)
        
        # Display results
        st.success(f"Total Grade: {grade}/100")
        st.write("Feedback:", feedback)
        
        # Save to CSV
        save_grade(full_name, student_id, grade)

def save_grade(full_name, student_id, grade):
    csv_path = "grades/data_submission.csv"
    
    # Create directory if it doesn't exist
    os.makedirs("grades", exist_ok=True)
    
    # Initialize or load the CSV
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=[
            "full_name", "student_id"] + 
            [f"assignment{i}" for i in range(1, 16)] +
            [f"quiz{i}" for i in range(1, 11)] +
            ["total"])
    else:
        df = pd.read_csv(csv_path)
    
    # Update or add new row
    student_row = df[df['student_id'] == student_id].index
    if len(student_row) > 0:
        df.loc[student_row, 'assignment1'] = grade
        # Recalculate total
        assignments = df.loc[student_row, [f'assignment{i}' for i in range(1, 16)]].fillna(0)
        quizzes = df.loc[student_row, [f'quiz{i}' for i in range(1, 11)]].fillna(0)
        df.loc[student_row, 'total'] = assignments.mean() * 0.7 + quizzes.mean() * 0.3
    else:
        new_row = pd.DataFrame({
            'full_name': [full_name],
            'student_id': [student_id],
            'assignment1': [grade]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    
    df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    main()

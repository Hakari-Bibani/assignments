import streamlit as st
import pandas as pd
import os
from grade1 import grade_assignment
import ast

def load_or_create_submissions():
    if not os.path.exists('grades'):
        os.makedirs('grades')
    
    file_path = 'grades/data_submission.csv'
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['name', 'student_id', 'total', 'week1'])
        df.to_csv(file_path, index=False)
    return pd.read_csv(file_path)

def save_submission(name, student_id, total_grade):
    df = load_or_create_submissions()
    
    # Check if student already submitted
    if len(df[(df['student_id'] == student_id) & (df['week1'].notna())]) > 0:
        st.error("You have already submitted this assignment!")
        return False
    
    # Add new submission
    new_row = {
        'name': name,
        'student_id': student_id,
        'total': total_grade,
        'week1': total_grade
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('grades/data_submission.csv', index=False)
    return True

def main():
    st.title("Week 1 - Mapping Coordinates and Calculating Distances")
    
    # Student Information
    st.subheader("Student Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    
    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        **Objective:** Create a Python script to plot three geographical coordinates and calculate distances.
        
        **Coordinates:**
        - Point 1: (36.325735, 43.928414)
        - Point 2: (36.393432, 44.586781)
        - Point 3: (36.660477, 43.840174)
        
        **Requirements:**
        1. Plot the coordinates on a map using folium
        2. Calculate distances between all points in kilometers
        3. Display results clearly
        """)
    
    # Code Submission
    st.subheader("Code Submission")
    code = st.text_area("Paste your code here", height=300)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Run Code"):
            if code.strip():
                try:
                    # Create a temporary Python file and execute it
                    with open('temp_submission.py', 'w') as f:
                        f.write(code)
                    
                    # Execute in try-except block to capture potential errors
                    try:
                        exec(code, globals())
                        st.success("Code executed successfully!")
                    except Exception as e:
                        st.error(f"Error executing code: {str(e)}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter code before running.")

    with col2:
        if st.button("Submit Assignment"):
            if not all([name, email, student_id, code]):
                st.error("Please fill in all fields before submitting.")
                return
            
            # Grade the submission
            total_grade = grade_assignment(code)
            
            # Save submission
            if save_submission(name, student_id, total_grade):
                st.success(f"Assignment submitted successfully! Grade: {total_grade}/100")
            
if __name__ == "__main__":
    main()

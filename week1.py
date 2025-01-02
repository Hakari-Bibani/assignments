import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
from pathlib import Path
import sys
import io
import contextlib
import ast
import inspect
import folium

# Helper functions
def load_or_create_grades_file():
    grades_file = Path("grades/data_submission.csv")
    grades_file.parent.mkdir(exist_ok=True)
    if not grades_file.exists():
        df = pd.DataFrame(columns=['name', 'student_id', 'total', 'week1'])
        df.to_csv(grades_file, index=False)
    return grades_file

def save_grade(name, student_id, total_grade):
    grades_file = load_or_create_grades_file()
    df = pd.read_csv(grades_file)
    if ((df['name'] == name) & (df['student_id'] == student_id)).any():
        df.loc[(df['name'] == name) & (df['student_id'] == student_id), 'week1'] = total_grade
        df.loc[(df['name'] == name) & (df['student_id'] == student_id), 'total'] = total_grade
    else:
        new_row = pd.DataFrame({
            'name': [name],
            'student_id': [student_id],
            'total': [total_grade],
            'week1': [total_grade]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(grades_file, index=False)

def extract_folium_map(namespace):
    """Extract Folium map object from namespace if it exists"""
    for obj in namespace.values():
        if isinstance(obj, folium.Map):
            return obj
    return None

def run():
    # Main page content
    st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")

    # Student Information
    st.header("Student Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")

    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        **Objective:** Create a Python script to plot three geographical coordinates on a map and calculate distances between points.
        
        **Required Libraries:**
        - geopy for distance calculations
        - folium for mapping
        
        **Coordinates:**
        - Point 1: (36.325735, 43.928414)
        - Point 2: (36.393432, 44.586781)
        - Point 3: (36.660477, 43.840174)
        
        **Requirements:**
        1. Plot all three points on an interactive map
        2. Calculate distances between each pair of points in kilometers
        """)

    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Paste your code here", height=300)

    col1, col2 = st.columns(2)

    # Run Code Button
    if col1.button("Run Code"):
        if code.strip():
            # Create a temporary file to save the map
            temp_html = "temp_map.html"
            namespace = {}
            try:
                # Add display function to namespace
                namespace['display'] = lambda x: None  # Mock display function
                
                # Execute student code
                exec(code, namespace)
                st.success("Code executed successfully!")
                
                # Find and save the map
                folium_map = extract_folium_map(namespace)
                if folium_map:
                    folium_map.save(temp_html)
                    with open(temp_html, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    html(html_content, height=500)
                    # Clean up
                    import os
                    if os.path.exists(temp_html):
                        os.remove(temp_html)
                        
                except Exception as e:
                    st.error(f"Error executing code: {str(e)}")
        else:
            st.warning("Please enter code before running")

    # Submit Assignment Button
    if col2.button("Submit Assignment"):
        if not all([name, email, student_id, code]):
            st.error("Please fill in all fields before submitting")
        else:
            try:
                # Import grading function
                from grade1 import grade_assignment
                
                # Grade the submission
                total_grade = grade_assignment(code)
                
                # Save grade to CSV
                save_grade(name, student_id, total_grade)
                
                st.success(f"Assignment submitted successfully! Total Grade: {total_grade}/100")
            except Exception as e:
                st.error(f"Error during submission: {str(e)}")

if __name__ == "__main__":
    run()

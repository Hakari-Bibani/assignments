import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from pages.style1 import execute_code, display_output
from grades.grade1 import grade_submission
import os

# Constants for coordinates
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Function to calculate distances
def calculate_distances(coords):
    try:
        dist1_2 = geodesic(coords[0], coords[1]).kilometers
        dist2_3 = geodesic(coords[1], coords[2]).kilometers
        dist1_3 = geodesic(coords[0], coords[2]).kilometers
        return {
            'Distance 1-2': round(dist1_2, 2),
            'Distance 2-3': round(dist2_3, 2),
            'Distance 1-3': round(dist1_3, 2)
        }
    except Exception as e:
        st.error(f"Error calculating distances: {str(e)}")
        return None

# Streamlit UI
st.title("Week 1 - Mapping Coordinates and Calculating Distances")

# Student Information
name = st.text_input("Full Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID (Optional)")

# Assignment Details Accordion
with st.expander("Assignment Details", expanded=True):
    st.markdown("""
    ### Objective:
    Write a Python script to plot three geographical coordinates on a map and calculate distances between them.
    
    ### Coordinates:
    - Point 1: (36.325735, 43.928414)
    - Point 2: (36.393432, 44.586781)
    - Point 3: (36.660477, 43.840174)
    
    ### Expected Output:
    1. A map showing all three points with markers
    2. Distance calculations between:
       - Point 1 and Point 2
       - Point 2 and Point 3
       - Point 1 and Point 3
    """)

# Code Input
st.markdown("### 📝 Code Cell")
code = st.text_area(
    "",
    height=200,
    placeholder="# Enter your code here...",
    help="Write or paste your Python code that implements the required functionality"
)

# Tabbed interface for Run/Submit
tabs = st.tabs(["Run Cell", "Submit Assignment"])

with tabs[0]:
    if st.button("▶ Run", type="primary"):
        if code.strip():
            st.markdown("### 📤 Output Cell")
            output, error, local_vars = execute_code(code)
            display_output(output, error)
            
            # Store map and distances in session state
            if local_vars:
                for var in local_vars:
                    if isinstance(local_vars[var], folium.Map):
                        st.session_state.map_obj = local_vars[var]
                        st.session_state.distances = calculate_distances(COORDINATES)
                        break

with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in Name and Email before submitting.")
        elif not code.strip():
            st.error("Please enter your code before submitting.")
        else:
            try:
                # Get grade from grading function
                score, breakdown = grade_submission(code)
                
                try:
                    # Read existing CSV with all columns
                    try:
                        df = pd.read_csv('grades/data_submission.csv')
                    except FileNotFoundError:
                        # Create DataFrame with all required columns if file doesn't exist
                        columns = ['Full Name', 'Email', 'Student ID'] + \
                                [f'assignment{i}' for i in range(1, 16)] + \
                                [f'quiz{i}' for i in range(1, 11)] + \
                                ['total']
                        df = pd.DataFrame(columns=columns)
                    
                    # Create new submission row with all columns initialized to 0
                    new_submission = {col: 0 for col in df.columns}  # Initialize all grade columns to 0
                    
                    # Update the basic info
                    new_submission.update({
                        'Full Name': name,
                        'Email': email,
                        'Student ID': student_id if student_id else 'N/A',
                        'assignment1': score  # Update assignment1 with the actual grade
                    })
                    
                    # Calculate new total (sum of all assignments and quizzes)
                    assignment_cols = [f'assignment{i}' for i in range(1, 16)]
                    quiz_cols = [f'quiz{i}' for i in range(1, 11)]
                    
                    # If student already exists, keep their other grades
                    existing_student = df[df['Email'] == email]
                    if not existing_student.empty:
                        for col in assignment_cols + quiz_cols:
                            if col != 'assignment1':  # Keep all grades except assignment1
                                new_submission[col] = existing_student.iloc[0][col]
                    
                    # Calculate total
                    grade_cols = assignment_cols + quiz_cols
                    new_submission['total'] = sum(new_submission[col] for col in grade_cols)
                    
                    # Remove existing record for this student if exists
                    df = df[df['Email'] != email]
                    
                    # Add new submission
                    df = pd.concat([df, pd.DataFrame([new_submission])], ignore_index=True)
                    
                    # Save updated DataFrame
                    df.to_csv('grades/data_submission.csv', index=False)
                    
                    # Display success message with grade and breakdown
                    st.success(f"Assignment submitted successfully!")
                    st.markdown(f"### Grade: {score}/100")
                    
                    # Display grade breakdown
                    st.markdown("### Grade Breakdown:")
                    for category, points in breakdown.items():
                        if isinstance(points, dict):
                            st.markdown(f"**{category}:**")
                            for subcategory, subpoints in points.items():
                                st.markdown(f"- {subcategory}: {subpoints:.2f} points")
                        else:
                            st.markdown(f"**{category}:** {points:.2f} points")
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Error saving submission: {str(e)}")
            except Exception as e:
                st.error(f"Error grading submission: {str(e)}")

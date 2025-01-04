import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output
import sys
import os

# Initialize session state for map and distances
if 'map_obj' not in st.session_state:
    st.session_state.map_obj = None
if 'distances' not in st.session_state:
    st.session_state.distances = None

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

# Code Input with Colab-like styling
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

# Replace the submission handling code in as1.py

# In the Submit tab section:
with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email or not student_id:  # Making student ID required
            st.error("Please fill in all fields (Name, Email, and Student ID).")
        elif not code.strip():
            st.error("Please enter your code before submitting.")
        else:
            try:
                # Execute and grade the code
                output, error, local_vars = execute_code(code)
                if error:
                    st.error(f"Error in code execution: {error}")
                else:
                    # Calculate grade using the grading module
                    grade, _ = grade_submission(code)
                    
                    try:
                        # Read existing CSV with all columns
                        df = pd.read_csv('grades/data_submission.csv')
                        
                        # Create new submission row with all required columns
                        new_submission = {
                            'fullname': name,
                            'email': email,
                            'studentID': student_id,
                            'assignment1': grade
                        }
                        
                        # Fill other assignments and quizzes with 0 or NaN
                        for col in df.columns:
                            if col not in new_submission:
                                new_submission[col] = 0  # or np.nan if you prefer
                                
                        # Check if student already exists
                        existing_student = df[df['studentID'] == student_id]
                        
                        if not existing_student.empty:
                            # Update existing student's assignment1 grade
                            df.loc[df['studentID'] == student_id, 'assignment1'] = grade
                        else:
                            # Add new student
                            df = pd.concat([df, pd.DataFrame([new_submission])], ignore_index=True)
                        
                        # Calculate total (sum of all assignments and quizzes)
                        assignment_cols = [col for col in df.columns if col.startswith('assignment')]
                        quiz_cols = [col for col in df.columns if col.startswith('quiz')]
                        df['total'] = df[assignment_cols + quiz_cols].sum(axis=1)
                        
                        # Save updated dataframe
                        df.to_csv('grades/data_submission.csv', index=False)
                        
                        st.success(f"Assignment submitted successfully! Grade: {grade}/100")
                        st.balloons()
                        
                    except FileNotFoundError:
                        st.error("Error: Grades file not found. Please contact your instructor.")
                    except Exception as e:
                        st.error(f"Error saving submission: {str(e)}")
                        
            except Exception as e:
                st.error(f"Error processing submission: {str(e)}")

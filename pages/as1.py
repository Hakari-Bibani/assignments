import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
import os
from pathlib import Path

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

# Function to get grades directory path
def get_grades_path():
    current_dir = Path(__file__).parent.parent
    grades_dir = current_dir / 'grades'
    return grades_dir / 'data_submission.csv'

# Add the grades directory to system path
grades_path = get_grades_path()
if not grades_path.parent.exists():
    grades_path.parent.mkdir(parents=True)

# Import grading function
sys.path.append(str(grades_path.parent))
from grade1 import grade_submission

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
            try:
                # Create a local namespace for execution
                local_dict = {}
                exec(code, {'folium': folium, 'geodesic': geodesic}, local_dict)
                
                # Store map and distances in session state
                for var in local_dict:
                    if isinstance(local_dict[var], folium.Map):
                        st.session_state.map_obj = local_dict[var]
                        st.session_state.distances = calculate_distances(COORDINATES)
                        break
                
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")

with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in Name and Email before submitting.")
        elif not code.strip():
            st.error("Please enter your code before submitting.")
        else:
            try:
                # Grade the submission
                grade, grade_details = grade_submission(code)
                
                # Read existing CSV file
                csv_path = get_grades_path()
                try:
                    df = pd.read_csv(csv_path)
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    # Create DataFrame with correct columns if file doesn't exist
                    df = pd.DataFrame(columns=[
                        'Full Name', 'Student ID', 'Email', 
                        'Assignment 1', 'Total'
                    ])

                # Create new submission row
                new_submission = pd.DataFrame({
                    'Full Name': [name],
                    'Student ID': [student_id if student_id else 'N/A'],
                    'Email': [email],
                    'Assignment 1': [code],
                    'Total': [grade]
                })

                # Remove previous submission if exists
                if not df.empty and 'Email' in df.columns:
                    df = df[df['Email'] != email]

                # Append new submission
                df = pd.concat([df, new_submission], ignore_index=True)

                # Save to CSV
                df.to_csv(csv_path, index=False)
                
                # Display results
                st.success(f"Assignment submitted successfully! Your grade is: {grade}/100")
                st.json(grade_details)
                st.balloons()
                
            except Exception as e:
                st.error(f"Error submitting assignment: {str(e)}")
                st.error(f"Error details: {type(e).__name__}: {str(e)}")

# Display the map and distances
if st.session_state.get('map_obj'):
    st_folium(st.session_state.map_obj, width=800, height=500)
    if st.session_state.get('distances'):
        st.markdown("### 📏 Distance Report")
        col1, col2, col3 = st.columns(3)
        col1.metric("Points 1-2", f"{st.session_state.distances['Distance 1-2']} km")
        col2.metric("Points 2-3", f"{st.session_state.distances['Distance 2-3']} km")
        col1.metric("Points 1-3", f"{st.session_state.distances['Distance 1-3']} km")

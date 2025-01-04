import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
import sys
from io import StringIO
import contextlib
import os

# Import grading function
sys.path.append('../grades')
from grade1 import grade_submission

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

# Function to capture print outputs
@contextlib.contextmanager
def capture_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out

def execute_code(code_string):
    """Execute code and capture its output"""
    with capture_output() as s:
        try:
            # Create a local namespace
            local_vars = {}
            # Execute the code
            exec(code_string, globals(), local_vars)
            # Get the printed output
            output = s.getvalue()
            return output, None, local_vars
        except Exception as e:
            return None, str(e), None

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
    "",  # Empty label to mimic Colab
    height=200,
    placeholder="# Enter your code here...",
    help="Write or paste your Python code that implements the required functionality"
)

# Store map object and distances in session state
if 'map_obj' not in st.session_state:
    st.session_state.map_obj = None
if 'distances' not in st.session_state:
    st.session_state.distances = None

# Tabbed interface for Run/Submit
tabs = st.tabs(["Run Cell", "Submit Assignment"])

with tabs[0]:
    if st.button("▶ Run", type="primary"):
        if code.strip():
            # Create output cell styling
            st.markdown("### 📤 Output Cell")
            
            # Execute the code
            output, error, local_vars = execute_code(code)
            
            if error:
                # Display error in red, similar to Colab
                st.markdown(f"""
                <div style='color: red; font-family: monospace; padding: 10px; 
                            background-color: #f8f9fa; border-left: 3px solid red;'>
                {error}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display regular output if any
                if output:
                    st.markdown(f"""
                    <div style='font-family: monospace; padding: 10px; 
                                background-color: #f8f9fa; border-left: 3px solid #2196F3;'>
                    {output}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Look for map object in local variables
                if local_vars:
                    for var in local_vars:
                        if isinstance(local_vars[var], folium.Map):
                            st.session_state.map_obj = local_vars[var]
                            # Calculate distances when map is found
                            st.session_state.distances = calculate_distances(COORDINATES)
                            break

ith tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in Name and Email before submitting.")
        elif not code.strip():
            st.error("Please enter your code before submitting.")
        else:
            try:
                # Grade the submission
                score, breakdown = grade_submission(code)

                # Create submission data
                submission_data = {
                    'Full Name': [name],
                    'Student ID': [student_id if student_id else 'N/A'],
                    'Email': [email],
                    'Assignment 1': [score],
                    'Total': [score]
                }

                # Ensure grades directory exists
                os.makedirs('grades', exist_ok=True)
                
                # Save to CSV
                try:
                    # Try to read existing CSV
                    df = pd.read_csv('grades/data_submission.csv')
                except FileNotFoundError:
                    # If file doesn't exist, create new DataFrame
                    df = pd.DataFrame(columns=['Full Name', 'Student ID', 'Email', 
                                            'Assignment 1', 'Total'])
                
                # Add new submission
                new_df = pd.DataFrame(submission_data)
                df = pd.concat([df, new_df], ignore_index=True)
                
                # Save to CSV
                df.to_csv('grades/data_submission.csv', index=False)

                # Display success message with score
                st.success(f"Assignment submitted successfully! Your grade: {score}/100")

                # Display score breakdown
                st.markdown("### Grade Breakdown:")
                
                # Code Structure
                st.markdown("#### 1. Code Structure and Implementation (30 points):")
                code_structure = breakdown['Code Structure']
                st.write(f"- Library Imports: {code_structure['Imports']:.1f}/5")
                st.write(f"- Coordinate Handling: {code_structure['Coordinates']:.1f}/5")
                st.write(f"- Code Execution: {code_structure['Execution']:.1f}/10")
                st.write(f"- Code Quality: {code_structure['Code Quality']:.1f}/10")

                # Map Visualization
                st.markdown("#### 2. Map Visualization (40 points):")
                st.write(f"- Score: {breakdown['Map Visualization']:.1f}/40")

                # Distance Calculations
                st.markdown("#### 3. Distance Calculations (30 points):")
                st.write(f"- Score: {breakdown['Distance Calculations']:.1f}/30")

                st.balloons()
                
            except Exception as e:
                st.error(f"Error submitting assignment: {str(e)}")
                st.error("Please try again or contact support if the problem persists.")

# Always display the map and distances if they exist in session state
if st.session_state.map_obj:
    st_folium(st.session_state.map_obj, width=800, height=500)
    
    if st.session_state.distances:
        st.markdown("### 📏 Distance Report")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Points 1-2", f"{st.session_state.distances['Distance 1-2']} km")
        with col2:
            st.metric("Points 2-3", f"{st.session_state.distances['Distance 2-3']} km")
        with col3:
            st.metric("Points 1-3", f"{st.session_state.distances['Distance 1-3']} km")

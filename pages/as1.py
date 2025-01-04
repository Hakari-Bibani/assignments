import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from pages.style1 import execute_code, display_output

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
                # Grade the submission using grade1.py
                score, breakdown = grade_submission(code)
                
                # Create full submission record with all assignments and quizzes initialized to 0
                submission = {
                    'Full Name': name,
                    'Email': email,
                    'Student ID': student_id if student_id else 'N/A'
                }
                
                # Initialize all assignments to 0
                for i in range(1, 16):  # Assignments 1-15
                    submission[f'Assignment {i}'] = 0
                
                # Initialize all quizzes to 0
                for i in range(1, 11):  # Quizzes 1-10
                    submission[f'Quiz {i}'] = 0
                
                # Update Assignment 1 with actual score
                submission['Assignment 1'] = score
                
                # Calculate total (sum of all assignments and quizzes)
                total = score  # Currently only Assignment 1 has a score
                submission['Total'] = total
                
                try:
                    # Try to read existing CSV file
                    df = pd.read_csv('grades/data_submission.csv')
                    
                    # Check if student already submitted
                    existing_submission = df[
                        (df['Email'] == email) & 
                        (df['Student ID'] == submission['Student ID'])
                    ]
                    
                    if not existing_submission.empty:
                        # Update existing submission
                        df.loc[existing_submission.index[0], 'Assignment 1'] = score
                        df.loc[existing_submission.index[0], 'Total'] = df.loc[
                            existing_submission.index[0],
                            [col for col in df.columns if col.startswith(('Assignment ', 'Quiz '))]
                        ].sum()
                    else:
                        # Add new submission
                        df = pd.concat([df, pd.DataFrame([submission])], ignore_index=True)
                        
                except FileNotFoundError:
                    # Create new DataFrame with all required columns if file doesn't exist
                    df = pd.DataFrame([submission])
                
                # Save to CSV
                df.to_csv('grades/data_submission.csv', index=False)
                
                # Display grade and breakdown
                st.success(f"Assignment submitted successfully! Grade: {score}/100")
                
                # Show detailed breakdown
                st.markdown("### Grade Breakdown:")
                
                # Code Structure
                st.markdown("**Code Structure and Implementation (30 points)**")
                structure_score = sum(breakdown["Code Structure"].values())
                st.write(f"- Imports: {breakdown['Code Structure']['Imports']:.1f}/5")
                st.write(f"- Coordinates: {breakdown['Code Structure']['Coordinates']:.1f}/5")
                st.write(f"- Execution: {breakdown['Code Structure']['Execution']}/10")
                st.write(f"- Code Quality: {breakdown['Code Structure']['Code Quality']}/10")
                st.write(f"Total Structure Score: {structure_score:.1f}/30")
                
                # Map Visualization
                st.markdown("**Map Visualization (40 points)**")
                st.write(f"Total Map Score: {breakdown['Map Visualization']}/40")
                
                # Distance Calculations
                st.markdown("**Distance Calculations (30 points)**")
                st.write(f"Total Distance Score: {breakdown['Distance Calculations']}/30")
                
                st.balloons()
                
            except Exception as e:
                st.error(f"Error submitting assignment: {str(e)}")

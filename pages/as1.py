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
                # Grade the student's code
                from grades.grade1 import grade_submission
                grade, breakdown = grade_submission(code)
                
                # Display the student's grade
                st.success(f"Your grade: {grade}/100")
                
                # Prepare the submission record
                submission = {
                    'Full name': name,
                    'email': email,
                    'student ID': student_id if student_id else 'N/A',
                    'assigment1': grade,
                    'total': grade  # Placeholder for now
                }
                
                # Load the CSV file or create a new DataFrame if it doesn't exist
                try:
                    df = pd.read_csv('grades/data_submission.csv')
                except FileNotFoundError:
                    df = pd.DataFrame(columns=['Full name', 'email', 'student ID', 'assigment1', 'total'])
                
                # Update or add the submission record
                if name in df['Full name'].values:
                    # Update existing record
                    df.loc[df['Full name'] == name, ['email', 'student ID', 'assigment1', 'total']] = [
                        email, student_id if student_id else 'N/A', grade, grade
                    ]
                else:
                    # Add new record
                    df = pd.concat([df, pd.DataFrame([submission])], ignore_index=True)
                
                # Save the updated CSV file
                df.to_csv('grades/data_submission.csv', index=False)
                
                # Success message
                st.success("Assignment submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error submitting assignment: {str(e)}")

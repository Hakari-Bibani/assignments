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
student_id = st.text_input("Student ID")

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
                output, error, local_vars = execute_code(code)
                if error:
                    st.error(f"Error in code execution: {error}")
                else:
                    submission = {
                        'Full Name': name,
                        'Student ID': student_id if student_id else 'N/A',
                        'Email': email,
                        'Assignment 1': 100,  # Placeholder score
                        'Total': 100
                    }
                    
                    try:
                        df = pd.read_csv('grades/data_submission.csv')
                    except FileNotFoundError:
                        df = pd.DataFrame(columns=['Full Name', 'Student ID', 'Email', 'Assignment 1', 'Total'])
                    
                    df = pd.concat([df, pd.DataFrame([submission])], ignore_index=True)
                    df.to_csv('grades/data_submission.csv', index=False)
                    
                    st.success("Assignment submitted successfully!")
                    st.balloons()
            except Exception as e:
                st.error(f"Error submitting assignment: {str(e)}")

# Display the map and distances
if st.session_state.get('map_obj'):
    st_folium(st.session_state.map_obj, width=800, height=500)
    if st.session_state.get('distances'):
        st.markdown("### 📏 Distance Report")
        col1, col2, col3 = st.columns(3)
        col1.metric("Points 1-2", f"{st.session_state.distances['Distance 1-2']} km")
        col2.metric("Points 2-3", f"{st.session_state.distances['Distance 2-3']} km")
        col3.metric("Points 1-3", f"{st.session_state.distances['Distance 1-3']} km")

import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
import sys
from io import StringIO
import contextlib
from style1 import style_output, display_error, display_map_and_distances

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
            local_vars = {}
            exec(code_string, globals(), local_vars)
            output = s.getvalue()
            return output, None, local_vars
        except Exception as e:
            return None, str(e), None

# Streamlit UI
st.title("Week 1 - Mapping Coordinates and Calculating Distances")

name = st.text_input("Full Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID (Optional)")

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

st.markdown("### 📝 Code Cell")
code = st.text_area(
    "",
    height=200,
    placeholder="# Enter your code here...",
    help="Write or paste your Python code that implements the required functionality"
)

if 'map_obj' not in st.session_state:
    st.session_state.map_obj = None
if 'distances' not in st.session_state:
    st.session_state.distances = None

tabs = st.tabs(["Run Cell", "Submit Assignment"])

with tabs[0]:
    if st.button("▶ Run", type="primary"):
        if code.strip():
            st.markdown("### 📤 Output Cell")
            output, error, local_vars = execute_code(code)
            if error:
                display_error(error)
            else:
                style_output(output)
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
                    st.error("Please fix the code before submitting.")
                else:
                    submission = {
                        'Full Name': name,
                        'Student ID': student_id if student_id else 'N/A',
                        'Email': email,
                        'Assignment 1': 100,
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

display_map_and_distances()

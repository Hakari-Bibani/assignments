import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output
import sys
sys.path.append('./grades')  # Add the grades directory to Python path
from grade1 import grade_submission 

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



# In the Submit tab section of as1.py, replace the submission code with:
with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email or not student_id:
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
                    # Calculate grade
                    grade, _ = grade_submission(code)
                    
                    # Read the existing CSV file
                    csv_path = 'grades/data_submission.csv'
                    df = pd.read_csv(csv_path)
                    
                    # Create a new row with all columns initialized to 0
                    new_row = pd.DataFrame([{col: 0 for col in df.columns}])
                    
                    # Update the specific fields
                    new_row['fullname'] = name
                    new_row['email'] = email
                    new_row['studentID'] = student_id
                    new_row['assignment1'] = grade
                    
                    # Add the new row to the DataFrame
                    df = pd.concat([df, new_row], ignore_index=True)
                    
                    # Save back to CSV
                    df.to_csv(csv_path, index=False)
                    
                    st.success(f"Assignment submitted successfully! Grade: {grade}/100")
                    st.balloons()
                    
            except Exception as e:
                st.error(f"Error saving submission: {str(e)}")

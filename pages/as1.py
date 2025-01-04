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
                    
                    # Prepare the data row
                    new_row = {
                        'fullname': name,
                        'email': email,
                        'studentID': student_id
                    }
                    
                    # Initialize all assignment and quiz columns to 0
                    for i in range(1, 16):  # assignments 1-15
                        new_row[f'assignment{i}'] = 0
                    for i in range(1, 11):  # quizzes 1-10
                        new_row[f'quiz{i}'] = 0
                        
                    # Set the current assignment grade
                    new_row['assignment1'] = grade
                    
                    # Calculate total
                    total = sum(new_row[f'assignment{i}'] for i in range(1, 16)) + \
                           sum(new_row[f'quiz{i}'] for i in range(1, 11))
                    new_row['total'] = total

                    try:
                        # Read existing CSV
                        df = pd.read_csv('grades/data_submission.csv')
                        
                        # Check if student already exists
                        student_mask = df['studentID'] == student_id
                        if student_mask.any():
                            # Update existing student's assignment1
                            df.loc[student_mask, 'assignment1'] = grade
                            # Recalculate total
                            assignments_sum = df.loc[student_mask, [f'assignment{i}' for i in range(1, 16)]].sum(axis=1)
                            quizzes_sum = df.loc[student_mask, [f'quiz{i}' for i in range(1, 11)]].sum(axis=1)
                            df.loc[student_mask, 'total'] = assignments_sum + quizzes_sum
                        else:
                            # Add new student
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                        
                        # Save to CSV
                        df.to_csv('grades/data_submission.csv', index=False)
                        st.success(f"Assignment submitted successfully! Grade: {grade}/100")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"Error saving to CSV: {str(e)}")
                        
            except Exception as e:
                st.error(f"Error processing submission: {str(e)}")

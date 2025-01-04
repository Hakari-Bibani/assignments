import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output

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

            # Check for a folium map and distances
            map_found = False
            if local_vars:
                for var_name, var_value in local_vars.items():
                    if isinstance(var_value, folium.Map):
                        st.session_state['map_obj'] = var_value
                        st.session_state['distances'] = calculate_distances(COORDINATES)
                        map_found = True
                        break
            
            if not map_found:
                st.warning("No map object found in your code.")
        else:
            st.error("Please enter your code before running.")

    # Replace the submission code section with this:

with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in both your Name and Email before submitting.")
        elif 'map_obj' not in st.session_state or 'distances' not in st.session_state:
            st.error("Please run your code and generate the map before submitting.")
        else:
            try:
                # Debug message
                st.write("Starting submission process...")
                
                # Grade the submission
                from grades.grade1 import grade_submission
                score, breakdown = grade_submission(code)
                st.write(f"Grade calculated: {score}")

                # Create submission data
                data = {
                    'Full name': [name.strip()],
                    'email': [email.strip()],
                    'student ID': [student_id.strip() if student_id else 'N/A'],
                    'assigment1': [score],
                    'total': [score]  # Initialize total
                }
                
                # Debug message
                st.write("Created submission data...")

                file_path = 'grades/data_submission.csv'
                
                try:
                    # Try to read existing CSV
                    st.write(f"Attempting to read {file_path}...")
                    existing_df = pd.read_csv(file_path)
                    st.write("Existing file read successfully")
                    
                    # Check if student exists and remove old entry
                    existing_df = existing_df[existing_df['Full name'] != name.strip()]
                    
                    # Add new submission
                    new_submission = pd.DataFrame(data)
                    final_df = pd.concat([existing_df, new_submission], ignore_index=True)
                    
                except FileNotFoundError:
                    st.write("No existing file found, creating new DataFrame...")
                    final_df = pd.DataFrame(data)

                # Debug: Show what we're about to save
                st.write("Data to be saved:")
                st.write(final_df)
                
                # Save to CSV with error handling
                try:
                    st.write(f"Attempting to save to {file_path}...")
                    final_df.to_csv(file_path, index=False)
                    st.write("File saved successfully")
                    
                    # Verify the save
                    verification_df = pd.read_csv(file_path)
                    st.write("Verification read successful. File contents:")
                    st.write(verification_df)
                    
                    st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error saving file: {str(e)}")
                    
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")
                st.write(f"Error type: {type(e)}")
                st.write(f"Error details: {str(e)}")
                import traceback
                st.write("Full error:", traceback.format_exc())

import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output
import os
from github import Github
from datetime import datetime
import base64

# Constants for coordinates
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Initialize GitHub connection
@st.cache_resource
def init_github():
    try:
        pat = st.secrets["GITHUB_PAT"]
        return Github(pat)
    except Exception as e:
        st.error(f"Error initializing GitHub connection: {str(e)}")
        return None

# Function to update CSV in GitHub
def update_github_csv(submission_data):
    try:
        g = init_github()
        if not g:
            return False, "GitHub connection failed"

        repo = g.get_repo(st.secrets["GITHUB_REPO"])  # format: "username/repository"
        file_path = "grades/data_submission.csv"
        
        try:
            # Try to get existing file
            contents = repo.get_contents(file_path)
            existing_data = base64.b64decode(contents.content).decode('utf-8')
            df = pd.read_csv(pd.StringIO(existing_data))
        except:
            # Create new DataFrame if file doesn't exist
            df = pd.DataFrame(columns=['fullname', 'email', 'studentID', 'assignment1', 'total'])

        # Update or append submission data
        new_data = pd.DataFrame([submission_data])
        if submission_data['fullname'] in df['fullname'].values:
            # Update existing record
            df.loc[df['fullname'] == submission_data['fullname']] = new_data.iloc[0]
        else:
            # Append new record
            df = pd.concat([df, new_data], ignore_index=True)

        # Recalculate total
        assignment_cols = [col for col in df.columns if col.startswith('assignment')]
        quiz_cols = [col for col in df.columns if col.startswith('quiz')]
        df['total'] = df[assignment_cols + quiz_cols].sum(axis=1)

        # Prepare commit
        csv_buffer = df.to_csv(index=False)
        commit_message = f"Update submission data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        if contents:
            repo.update_file(
                file_path,
                commit_message,
                csv_buffer,
                contents.sha
            )
        else:
            repo.create_file(
                file_path,
                commit_message,
                csv_buffer
            )

        return True, "Submission successfully saved"
    except Exception as e:
        return False, f"Error updating GitHub: {str(e)}"

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

    # Display the map and distances if available
    if 'map_obj' in st.session_state:
        st.markdown("### 🗺️ Generated Map")
        st_folium(st.session_state['map_obj'], width=800, height=500)

    if 'distances' in st.session_state:
        st.markdown("### 📏 Distance Report")
        col1, col2, col3 = st.columns(3)
        col1.metric("Points 1-2", f"{st.session_state['distances']['Distance 1-2']} km")
        col2.metric("Points 2-3", f"{st.session_state['distances']['Distance 2-3']} km")
        col3.metric("Points 1-3", f"{st.session_state['distances']['Distance 1-3']} km")

with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in both your Name and Email before submitting.")
        elif 'map_obj' not in st.session_state or 'distances' not in st.session_state:
            st.error("Please run your code and generate the map before submitting.")
        else:
            try:
                # Grade the submission
                from grades.grade1 import grade_submission
                score, breakdown = grade_submission(code)

                # Prepare submission dictionary
                submission = {
                    'fullname': name.strip(),
                    'email': email.strip(),
                    'studentID': student_id.strip() if student_id else 'N/A',
                    'assignment1': score
                }

                # Update GitHub CSV
                success, message = update_github_csv(submission)
                
                if success:
                    st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                    st.balloons()
                    
                    # Display detailed feedback
                    st.markdown("### Grading Breakdown")
                    for criterion, points in breakdown.items():
                        st.write(f"- {criterion}: {points} points")
                else:
                    st.error(f"❌ Submission Error: {message}")
                    
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")

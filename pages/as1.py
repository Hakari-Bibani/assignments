import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output
from github import Github
import base64
import os
from datetime import datetime

# Constants
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Try to get GitHub secrets, fall back to local file if not available
try:
    GITHUB_REPO = st.secrets["github"]["repo"]
    PAT = st.secrets["github"]["pat"]
    USE_GITHUB = True
except KeyError:
    USE_GITHUB = False
    st.warning("GitHub secrets not configured. Falling back to local file storage.")

def update_github_csv(submission_data):
    """
    Update the CSV file in GitHub repository
    """
    try:
        # Initialize GitHub with PAT
        g = Github(PAT)
        repo = g.get_repo(GITHUB_REPO)
        
        file_path = 'grades/data_submission.csv'
        try:
            # Try to get existing file
            contents = repo.get_contents(file_path)
            existing_data = base64.b64decode(contents.content).decode('utf-8')
            
            # Load existing data into DataFrame
            df = pd.read_csv(pd.StringIO(existing_data))
            
            # Update or add new submission
            if submission_data['Full name'] in df['Full name'].values:
                # Update existing student's data
                df.loc[df['Full name'] == submission_data['Full name'], 
                      ['email', 'student ID', 'assignment1']] = [
                          submission_data['email'],
                          submission_data['student ID'],
                          submission_data['assignment1']
                      ]
            else:
                # Add new student data
                new_row = pd.DataFrame([submission_data])
                df = pd.concat([df, new_row], ignore_index=True)
            
            # Recalculate total
            assignment_cols = [col for col in df.columns if col.startswith(('assignment', 'quiz'))]
            df['total'] = df[assignment_cols].sum(axis=1)
            
            # Convert updated DataFrame to CSV string
            updated_csv = df.to_csv(index=False)
            
            # Create commit message
            commit_message = f"Update submission data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Update file in repository
            repo.update_file(
                file_path,
                commit_message,
                updated_csv,
                contents.sha
            )
            return True, "Submission successfully saved to GitHub"
            
        except Exception as e:
            return False, f"Error updating GitHub: {str(e)}"
            
    except Exception as e:
        return False, f"Error connecting to GitHub: {str(e)}"

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
                    'Full name': name.strip(),
                    'email': email.strip(),
                    'student ID': student_id.strip() if student_id else 'N/A',
                    'assignment1': score
                }

                if USE_GITHUB:
                    # Update GitHub with new submission
                    success, message = update_github_csv(submission)
                else:
                    # Fallback to local file storage
                    file_path = 'grades/data_submission.csv'
                    try:
                        # Try reading the existing CSV
                        if os.path.exists(file_path):
                            df = pd.read_csv(file_path)
                        else:
                            df = pd.DataFrame(columns=['Full name', 'email', 'student ID', 'assignment1', 'total'])

                        # Update or add the submission
                        if submission['Full name'] in df['Full name'].values:
                            df.loc[df['Full name'] == submission['Full name'], 
                                  ['email', 'student ID', 'assignment1']] = [
                                      submission['email'],
                                      submission['student ID'],
                                      submission['assignment1']
                                  ]
                        else:
                            new_row = pd.DataFrame([submission])
                            df = pd.concat([df, new_row], ignore_index=True)

                        # Recalculate the total column
                        assignment_cols = [col for col in df.columns if col.startswith(('assignment', 'quiz'))]
                        df['total'] = df[assignment_cols].sum(axis=1)

                        # Save the updated DataFrame
                        df.to_csv(file_path, index=False)
                        success, message = True, "Submission saved to local file"
                    except Exception as e:
                        success, message = False, f"Error saving to local file: {str(e)}"
                
                if success:
                    st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                    st.balloons()
                else:
                    st.error(f"❌ Error during submission: {message}")
                    
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")

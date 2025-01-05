import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output
import base64
from github import Github
from datetime import datetime
import io

# Constants for coordinates
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# GitHub Configuration
def init_github():
    try:
        return Github(st.secrets["github"]["pat"])
    except Exception as e:
        st.error(f"Error initializing GitHub: {str(e)}")
        return None

def update_github_csv(data_df):
    try:
        g = init_github()
        if not g:
            return False
        
        repo = g.get_repo(st.secrets["github"]["repository"])
        file_path = 'grades/data_submission.csv'
        
        try:
            # Try to get the existing file
            contents = repo.get_contents(file_path)
            # Convert DataFrame to CSV string
            csv_buffer = io.StringIO()
            data_df.to_csv(csv_buffer, index=False)
            csv_content = csv_buffer.getvalue()
            
            # Update file in GitHub
            repo.update_file(
                file_path,
                f"Update submission data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                csv_content,
                contents.sha
            )
            return True
        except Exception as e:
            st.error(f"Error updating GitHub file: {str(e)}")
            return False
    except Exception as e:
        st.error(f"GitHub operation failed: {str(e)}")
        return False

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

    # Display the map and distances if available in st.session_state
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
        if not name or not email or not student_id:
            st.error("Please fill in your Name, Email, and Student ID before submitting.")
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
                    'studentID': student_id.strip(),
                    'assignment1': score
                }

                try:
                    # Initialize GitHub connection
                    g = init_github()
                    if not g:
                        st.error("Failed to initialize GitHub connection")
                        return

                    repo = g.get_repo(st.secrets["github"]["repository"])
                    file_path = 'grades/data_submission.csv'

                    try:
                        # Get existing content
                        contents = repo.get_contents(file_path)
                        existing_data = pd.read_csv(io.StringIO(contents.decoded_content.decode()))
                    except:
                        # Create new DataFrame if file doesn't exist
                        existing_data = pd.DataFrame(columns=['fullname', 'email', 'studentID'] + 
                                                          [f'assignment{i}' for i in range(1, 16)] +
                                                          [f'quiz{i}' for i in range(1, 11)] +
                                                          ['total'])

                    # Update or add the submission
                    if submission['fullname'] in existing_data['fullname'].values:
                        # Update existing student's data
                        idx = existing_data.index[existing_data['fullname'] == submission['fullname']][0]
                        existing_data.loc[idx, 'email'] = submission['email']
                        existing_data.loc[idx, 'studentID'] = submission['studentID']
                        existing_data.loc[idx, 'assignment1'] = submission['assignment1']
                    else:
                        # Add new student data
                        new_row = pd.Series(index=existing_data.columns)
                        new_row['fullname'] = submission['fullname']
                        new_row['email'] = submission['email']
                        new_row['studentID'] = submission['studentID']
                        new_row['assignment1'] = submission['assignment1']
                        existing_data = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)

                    # Calculate total
                    assignment_cols = [col for col in existing_data.columns if col.startswith('assignment')]
                    quiz_cols = [col for col in existing_data.columns if col.startswith('quiz')]
                    existing_data['total'] = existing_data[assignment_cols + quiz_cols].sum(axis=1, skipna=True)

                    # Update the file in GitHub
                    if update_github_csv(existing_data):
                        st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                        st.balloons()
                    else:
                        st.error("Failed to update submission data in GitHub")

                except Exception as e:
                    st.error(f"Error during submission process: {str(e)}")

            except Exception as e:
                st.error(f"❌ Error during grading: {str(e)}")

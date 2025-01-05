import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output
import requests
import base64
import io  # Import io for StringIO

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

# Function to update CSV file in GitHub repository
def update_csv_in_github(submission):
    try:
        # GitHub API URL for the CSV file
        repo = "Hakari-Bibani/assignments"  # Updated repository name
        path = "grades/data_submission.csv"
        url = f"https://api.github.com/repos/{repo}/contents/{path}"

        # Headers for GitHub API
        headers = {
            "Authorization": f"Bearer {st.secrets['GITHUB_PAT']}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Try to get the current file content and SHA
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            # File does not exist, create a new DataFrame
            df = pd.DataFrame(columns=['fullname', 'email', 'studentID', 'assignment1', 'total'])
        else:
            response.raise_for_status()
            file_data = response.json()
            file_content = base64.b64decode(file_data['content']).decode('utf-8')
            df = pd.read_csv(io.StringIO(file_content))  # Use io.StringIO instead of pandas.compat.StringIO

        # Update or add the submission
        if submission['Full name'] in df['fullname'].values:
            # Update existing student's data
            df.loc[df['fullname'] == submission['Full name'], ['email', 'studentID', 'assignment1']] = \
                [submission['email'], submission['student ID'], submission['assignment1']]
        else:
            # Add new student data
            new_row = pd.DataFrame([{
                'fullname': submission['Full name'],
                'email': submission['email'],
                'studentID': submission['student ID'],
                'assignment1': submission['assignment1'],
                'total': submission['assignment1']  # Initialize total with assignment1 score
            }])
            df = pd.concat([df, new_row], ignore_index=True)

        # Recalculate the 'total' column as the sum of assignment scores
        df['total'] = df.filter(like='assignment').sum(axis=1)

        # Convert the updated DataFrame back to CSV
        updated_csv_content = df.to_csv(index=False)

        # Encode the updated content to base64
        updated_content_base64 = base64.b64encode(updated_csv_content.encode('utf-8')).decode('utf-8')

        # Commit the updated file to GitHub
        commit_data = {
            "message": f"Update data_submission.csv for {submission['Full name']}",
            "content": updated_content_base64,
            "sha": response.json()['sha'] if response.status_code != 404 else None
        }
        commit_response = requests.put(url, headers=headers, json=commit_data)
        commit_response.raise_for_status()

        return True
    except Exception as e:
        st.error(f"Error updating CSV in GitHub: {str(e)}")
        return False

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

                # Update the CSV file in GitHub
                if update_csv_in_github(submission):
                    st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                    st.balloons()
                else:
                    st.error("❌ Failed to update submission data in GitHub.")
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")

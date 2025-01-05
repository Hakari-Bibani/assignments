import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from github import Github
import time

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

# Function to check GitHub API rate limits
def check_rate_limit(github_client):
    try:
        rate_limit = github_client.get_rate_limit()
        core_limit = rate_limit.core  # Access the 'core' attribute
        remaining = core_limit.remaining
        reset_time = core_limit.reset
        st.write(f"Remaining API requests: {remaining}")
        st.write(f"Rate limit resets at: {reset_time}")
        return remaining, reset_time
    except Exception as e:
        st.error(f"❌ Error checking rate limit: {e}")
        return None, None

# Function to wait for rate limit reset
def wait_for_rate_limit_reset(reset_time):
    current_time = time.time()
    wait_seconds = reset_time.timestamp() - current_time
    if wait_seconds > 0:
        st.write(f"Waiting for rate limit reset: {wait_seconds:.2f} seconds")
        time.sleep(wait_seconds)

# Function to save submission to GitHub
def save_to_github_with_rate_limit(file_path, local_path):
    try:
        PAT = st.secrets["GITHUB_PAT"]
        if not PAT:
            raise ValueError("PAT is missing in secrets.toml.")

        github = Github(PAT)

        # Check rate limits
        remaining, reset_time = check_rate_limit(github)
        if remaining == 0:
            wait_for_rate_limit_reset(reset_time)

        repo = github.get_repo("Hakari-Bibani/assignments")
        with open(local_path, "r") as f:
            content = f.read()

        # Update or create file in GitHub repository
        try:
            file = repo.get_contents(file_path)
            repo.update_file(file.path, "Update submission data", content, file.sha)
        except Exception as e:
            if "Not Found" in str(e):
                repo.create_file(file_path, "Create submission data", content)
            else:
                raise e

        st.success("✅ Submission data saved successfully to GitHub.")
    except Exception as e:
        st.error(f"❌ Error saving submission: {e}")

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
        if not name or not email:
            st.error("Please fill in both your Name and Email before submitting.")
        elif 'map_obj' not in st.session_state or 'distances' not in st.session_state:
            st.error("Please run your code and generate the map before submitting.")
        else:
            try:
                # Save submission data
                submission_data = {
                    "fullname": name.strip(),
                    "email": email.strip(),
                    "studentID": student_id.strip() if student_id else "N/A",
                    "assignment1": st.session_state['distances']
                }
                file_path = "grades/data_submission.csv"

                # Save locally and upload to GitHub
                local_path = file_path
                save_to_github_with_rate_limit(file_path, local_path)
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")

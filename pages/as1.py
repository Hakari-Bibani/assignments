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

def calculate_distances(coords):
    """Calculate distances between given coordinates."""
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

def save_submission(name, email, student_id, score, file_path='grades/data_submission.csv'):
    """
    Save or update student submission data in the CSV file.
    """
    try:
        # Input validation
        if not name or not email:
            return False, "Name and email are required"
        
        name = name.strip()
        email = email.strip()
        student_id = student_id.strip() if student_id else 'N/A'
        
        # Prepare submission data
        submission = {
            'Full name': name,
            'email': email,
            'student ID': student_id,
            'assigment1': float(score)
        }
        
        try:
            # Try reading existing CSV
            df = pd.read_csv(file_path)
            
            # Verify column structure
            required_cols = ['Full name', 'email', 'student ID', 'assigment1', 'total']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return False, f"CSV file missing required columns: {missing_cols}"
                
        except FileNotFoundError:
            # Create new DataFrame if file doesn't exist
            df = pd.DataFrame(columns=['Full name', 'email', 'student ID', 'assigment1', 'total'])
        
        # Check for existing submission
        if name in df['Full name'].values:
            # Update existing record
            df.loc[df['Full name'] == name, ['email', 'student ID', 'assigment1']] = \
                [email, student_id, score]
            update_msg = "Submission updated"
        else:
            # Add new record
            new_row = pd.DataFrame([submission])
            df = pd.concat([df, new_row], ignore_index=True)
            update_msg = "New submission added"
            
        # Recalculate total column
        df['total'] = df.filter(like='assigment').sum(axis=1)
        
        # Save to CSV
        df.to_csv(file_path, index=False)
        
        return True, f"{update_msg} successfully"
        
    except Exception as e:
        return False, f"Error saving submission: {str(e)}"

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
                
                # Save the submission
                success, message = save_submission(name, email, student_id, score)
                
                if success:
                    st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")
                    
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")

# pages/as1.py
import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
import sys
from io import StringIO
import contextlib

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
            # Create a local namespace
            local_vars = {}
            # Execute the code
            exec(code_string, globals(), local_vars)
            # Get the printed output
            output = s.getvalue()
            return output, None, local_vars
        except Exception as e:
            return None, str(e), None

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
    "",  # Empty label to mimic Colab
    height=200,
    placeholder="# Enter your code here...",
    help="Write or paste your Python code that implements the required functionality"
)

# Store map object in session state
if 'map_obj' not in st.session_state:
    st.session_state.map_obj = None

# Tabbed interface for Run/Submit
tabs = st.tabs(["Run Cell", "Submit Assignment"])

with tabs[0]:
    if st.button("▶ Run", type="primary"):
        if code.strip():
            # Create output cell styling
            st.markdown("### 📤 Output Cell")
            
            # Execute the code
            output, error, local_vars = execute_code(code)
            
            if error:
                # Display error in red, similar to Colab
                st.markdown(f"""
                <div style='color: red; font-family: monospace; padding: 10px; 
                            background-color: #f8f9fa; border-left: 3px solid red;'>
                {error}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display regular output if any
                if output:
                    st.markdown(f"""
                    <div style='font-family: monospace; padding: 10px; 
                                background-color: #f8f9fa; border-left: 3px solid #2196F3;'>
                    {output}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Look for map object in local variables
                if local_vars:
                    for var in local_vars:
                        if isinstance(local_vars[var], folium.Map):
                            st.session_state.map_obj = local_vars[var]
                            break

            # Display map if it exists in session state
            if st.session_state.map_obj:
                st_folium(st.session_state.map_obj, width=800, height=500)

with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in Name and Email before submitting.")
        elif not code.strip():
            st.error("Please enter your code before submitting.")
        else:
            try:
                # Execute code to get results
                output, error, local_vars = execute_code(code)
                
                if error:
                    st.error(f"Error in code execution: {error}")
                    st.error("Please fix the code before submitting.")
                else:
                    # Save to CSV
                    submission = {
                        'Full Name': name,
                        'Student ID': student_id if student_id else 'N/A',
                        'Email': email,
                        'Assignment 1': 100,  # Placeholder score
                        'Total': 100  # Placeholder total
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

# Always display the map if it exists in session state
if st.session_state.map_obj:
    st_folium(st.session_state.map_obj, width=800, height=500)

# pages/as1.py
import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
import sys
from io import StringIO
import contextlib

# Store map and distances in session state
if 'map_obj' not in st.session_state:
    st.session_state.map_obj = None
if 'distances' not in st.session_state:
    st.session_state.distances = None

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
            
            # Look for map object and distances in local variables
            map_obj = None
            distances = None
            
            for var in local_vars:
                if isinstance(local_vars[var], folium.Map):
                    map_obj = local_vars[var]
                if var == 'distances' and isinstance(local_vars[var], (list, tuple)):
                    distances = local_vars[var]
            
            # Store in session state
            st.session_state.map_obj = map_obj
            st.session_state.distances = distances
            
            return output, None, map_obj, distances
        except Exception as e:
            return None, str(e), None, None

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
    
    ### Sample Code Structure:
    ```python
    import folium
    from geopy.distance import geodesic
    
    # Define coordinates
    coords = [
        (36.325735, 43.928414),  # Point 1
        (36.393432, 44.586781),  # Point 2
        (36.660477, 43.840174)   # Point 3
    ]
    
    # Create map centered on the middle point
    m = folium.Map(location=[36.5, 44], zoom_start=9)
    
    # Add markers for each point
    for i, coord in enumerate(coords, 1):
        folium.Marker(
            coord,
            popup=f'Point {i}',
            icon=folium.Icon(color='red')
        ).add_to(m)
    
    # Calculate distances
    dist1_2 = geodesic(coords[0], coords[1]).kilometers
    dist2_3 = geodesic(coords[1], coords[2]).kilometers
    dist1_3 = geodesic(coords[0], coords[2]).kilometers
    
    # Store distances in a list
    distances = [dist1_2, dist2_3, dist1_3]
    
    # Display map
    m
    
    # Print distances
    print(f"Distance between Point 1 and Point 2: {dist1_2:.2f} km")
    print(f"Distance between Point 2 and Point 3: {dist2_3:.2f} km")
    print(f"Distance between Point 1 and Point 3: {dist1_3:.2f} km")
    ```
    """)

# Code Input with Colab-like styling
st.markdown("### 📝 Code Cell")
code = st.text_area(
    "",  # Empty label to mimic Colab
    height=200,
    placeholder="# Enter your code here...",
    help="Write or paste your Python code that implements the required functionality"
)

# Tabbed interface for Run/Submit
tabs = st.tabs(["Run Cell", "Submit Assignment"])

with tabs[0]:
    if st.button("▶ Run", type="primary"):
        if code.strip():
            # Create output cell styling
            st.markdown("### 📤 Output Cell")
            output_placeholder = st.empty()
            
            # Execute the code
            output, error, map_obj, distances = execute_code(code)
            
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
                
                # Display map if available
                if map_obj:
                    st_folium(map_obj, width=800, height=500)
                
                # Display distances if available
                if distances:
                    st.markdown("### Distance Calculations:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Points 1-2", f"{distances[0]:.2f} km")
                    with col2:
                        st.metric("Points 2-3", f"{distances[1]:.2f} km")
                    with col3:
                        st.metric("Points 1-3", f"{distances[2]:.2f} km")

with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in Name and Email before submitting.")
        elif not code.strip():
            st.error("Please enter your code before submitting.")
        else:
            # Save submission
            try:
                # Get results from session state
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

import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
import sys
from io import StringIO
import contextlib

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

# Store map object and distances in session state
if 'map_obj' not in st.session_state:
    st.session_state.map_obj = None
if 'distances' not in st.session_state:
    st.session_state.distances = None

# Always display the map and distances if they exist in session state
if st.session_state.map_obj:
    st_folium(st.session_state.map_obj, width=800, height=500)
    
    if st.session_state.distances:
        st.markdown("### 📏 Distance Report")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Points 1-2", f"{st.session_state.distances['Distance 1-2']} km")
        with col2:
            st.metric("Points 2-3", f"{st.session_state.distances['Distance 2-3']} km")
        with col3:
            st.metric("Points 1-3", f"{st.session_state.distances['Distance 1-3']} km")

# pages/as1.py
import streamlit as st
import pandas as pd
import sys
import io
import json
import os
import importlib.util
import folium
from geopy.distance import geodesic

[Previous imports and import_grader() function remain the same...]

def main():
    [Previous student information and assignment details remain the same...]

    # Add template code
    st.subheader("Code Template")
    with st.expander("Click to see template code", expanded=False):
        st.code("""
import folium
from geopy.distance import geodesic

# Create a map centered on Kurdistan Region
m = folium.Map(location=[36.459477, 44.186757], zoom_start=9)

# Define the coordinates
point1 = (36.325735, 43.928414)  # Point 1
point2 = (36.393432, 44.586781)  # Point 2
point3 = (36.660477, 43.840174)  # Point 3

# Add markers for each point
folium.Marker(
    point1,
    popup='Point 1',
    icon=folium.Icon(color='red')
).add_to(m)

folium.Marker(
    point2,
    popup='Point 2',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    point3,
    popup='Point 3',
    icon=folium.Icon(color='green')
).add_to(m)

# Add lines connecting the points
folium.PolyLine(
    locations=[point1, point2, point3, point1],
    weight=2,
    color='red',
    opacity=0.8
).add_to(m)

# Calculate distances
dist_1_2 = geodesic(point1, point2).kilometers
dist_2_3 = geodesic(point2, point3).kilometers
dist_1_3 = geodesic(point1, point3).kilometers

# Print distances
print(f"Distance between Point 1 and Point 2: {dist_1_2:.2f} km")
print(f"Distance between Point 2 and Point 3: {dist_2_3:.2f} km")
print(f"Distance between Point 1 and Point 3: {dist_1_3:.2f} km")

# The map will be displayed automatically in Streamlit
        """)

    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Paste your code here:", height=300)
    
    # Run Code Logic
    if run_button and code:
        try:
            # Create a clean namespace for execution
            namespace = {
                'folium': folium,
                'geodesic': geodesic,
                'print': print,
                '__name__': '__main__'
            }
            
            # Capture output
            old_stdout = sys.stdout
            redirected_output = io.StringIO()
            sys.stdout = redirected_output

            # Execute the code
            exec(code, namespace)
            
            # Restore stdout
            sys.stdout = old_stdout
            
            # Display output
            st.subheader("Output:")
            output = redirected_output.getvalue()
            if output:
                st.text(output)

            # Display map if 'm' variable exists
            if 'm' in namespace and isinstance(namespace['m'], folium.Map):
                st.subheader("Map:")
                folium_map = namespace['m']
                map_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp_map.html")
                folium_map.save(map_path)
                with open(map_path, "r") as f:
                    st.components.v1.html(f.read(), height=500)
                os.remove(map_path)

        except Exception as e:
            st.error(f"Error executing code: {str(e)}")

    [Rest of the submit logic remains the same...]

if __name__ == "__main__":
    main()

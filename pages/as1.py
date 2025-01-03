# pages/as1.py
import streamlit as st
import pandas as pd
import sys
import io
import os
import folium
from geopy.distance import geodesic

def import_grader():
    grade_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'grades', 'grade1.py')
    spec = importlib.util.spec_from_file_location("grade1", grade_path)
    grade_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grade_module)
    return grade_module.grade_assignment

grade_assignment = import_grader()

def main():
    st.title("Week 1 Assignment - Mapping Coordinates and Calculating Distances")
    
    # Student Information
    st.header("Student Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        full_name = st.text_input("Full Name")
    with col2:
        email = st.text_input("Email")
    with col3:
        student_id = st.text_input("Student ID")

    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        **Objective:** Write a Python script to plot three geographical coordinates on a map and calculate 
        the distance between each pair of points in kilometers.
        
        **Task Requirements:**
        1. **Plot the Three Coordinates on a Map:**
           - Plot three locations in the Kurdistan Region
           - Use Python libraries to display points on a map
           
        2. **Calculate the Distance Between Each Pair of Points:**
           - Calculate distances in **kilometers**:
             - Distance between Point 1 and Point 2
             - Distance between Point 2 and Point 3
             - Distance between Point 1 and Point 3
        
        **Coordinates:**
        - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
        - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
        - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
        
        **Required Libraries:**
        ```python
        import folium
        from geopy.distance import geodesic
        ```
        """)

    # Code template without IPython dependencies
    st.subheader("Code Template")
    with st.expander("Click to see template code", expanded=False):
        st.code("""
# Required imports (already available in the environment)
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
""")

    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Paste your code here:", height=300)
    
    # Buttons for Run and Submit
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("Run Code")
    with col2:
        submit_button = st.button("Submit Assignment")

    # Run Code Logic
    if run_button and code:
        try:
            # Set up the execution environment
            namespace = {
                'folium': folium,
                'geodesic': geodesic,
                'print': print,
            }
            
            # Capture output
            output_buffer = io.StringIO()
            sys.stdout = output_buffer

            # Execute the code
            exec(code, namespace)
            
            # Restore stdout
            sys.stdout = sys.__stdout__
            
            # Display output
            st.subheader("Output:")
            output = output_buffer.getvalue()
            if output:
                st.text(output)

            # Display map if it exists
            if 'm' in namespace and isinstance(namespace['m'], folium.Map):
                st.subheader("Map Visualization:")
                map_data = namespace['m']._repr_html_()
                st.components.v1.html(map_data, height=500)

        except Exception as e:
            st.error(f"Error executing code: {str(e)}")
            sys.stdout = sys.__stdout__  # Ensure stdout is restored

    # Submit Logic
    if submit_button:
        if not all([full_name, email, student_id, code]):
            st.error("Please fill in all fields before submitting.")
            return

        try:
            # Grade the submission
            grade, feedback = grade_assignment(code)
            
            # Display results
            st.success(f"Assignment submitted successfully! Grade: {grade}/100")
            st.write("Feedback:", feedback)
            
            # Save grade to CSV
            grades_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'grades')
            csv_path = os.path.join(grades_dir, 'data_submission.csv')
            
            try:
                df = pd.read_csv(csv_path)
            except FileNotFoundError:
                columns = ['Full name', 'student ID'] + \
                         [f'assignment{i}' for i in range(1, 16)] + \
                         [f'quiz{i}' for i in range(1, 11)] + ['total']
                df = pd.DataFrame(columns=columns)
            
            # Update or add new row
            if student_id in df['student ID'].values:
                df.loc[df['student ID'] == student_id, 'assignment1'] = grade
            else:
                new_row = pd.DataFrame({
                    'Full name': [full_name],
                    'student ID': [student_id],
                    'assignment1': [grade]
                })
                df = pd.concat([df, new_row], ignore_index=True)
            
            # Calculate total
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
            df['total'] = df[numeric_columns].sum(axis=1)
            
            # Save to CSV
            df.to_csv(csv_path, index=False)

        except Exception as e:
            st.error(f"Error during submission: {str(e)}")

if __name__ == "__main__":
    main()

import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
from pathlib import Path
import sys
import io
import contextlib
import ast
import inspect
import folium
from geopy.distance import geodesic

# Grading functions from grade1.py
def check_imports(code_str):
    """Check if required libraries are imported"""
    try:
        tree = ast.parse(code_str)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(n.name for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        
        required_libs = {'geopy', 'folium'}
        found_libs = set(imports)
        
        return len(required_libs.intersection(found_libs)) * 2.5  # 5 points total
    except:
        return 0

def check_coordinates(code_str):
    """Check if coordinates are correctly specified"""
    correct_coords = [
        (36.325735, 43.928414),
        (36.393432, 44.586781),
        (36.660477, 43.840174)
    ]
    
    try:
        tree = ast.parse(code_str)
        found_coords = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Tuple):
                if len(node.elts) == 2:
                    try:
                        lat = float(node.elts[0].value)
                        lon = float(node.elts[1].value)
                        found_coords.append((lat, lon))
                    except:
                        continue
        
        points = 0
        for coord in correct_coords:
            if any(abs(c[0] - coord[0]) < 0.0001 and abs(c[1] - coord[1]) < 0.0001 
                  for c in found_coords):
                points += 1.67
        
        return points  # 5 points total
    except:
        return 0

def check_distance_calculations(code_str):
    """Check if distances are calculated correctly"""
    correct_distances = {
        (0, 1): 59.57,  # Point 1 to Point 2
        (1, 2): 73.14,  # Point 2 to Point 3
        (0, 2): 37.98   # Point 1 to Point 3
    }
    
    try:
        # Execute code in controlled environment
        locals_dict = {}
        exec(code_str, {'geodesic': geodesic}, locals_dict)
        
        # Look for values close to correct distances
        points = 0
        for values in locals_dict.values():
            if isinstance(values, (int, float)):
                for correct_dist in correct_distances.values():
                    if abs(values - correct_dist) < 0.1:
                        points += 6.67  # 20 points total / 3 distances
        
        return min(points, 20)
    except:
        return 0

def check_map_visualization(code_str):
    """Check map visualization implementation"""
    try:
        tree = ast.parse(code_str)
        points = 0
        
        # Check for folium.Map creation
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr == 'Map':
                    points += 15
                elif hasattr(node.func, 'attr') and node.func.attr == 'Marker':
                    points += 5  # Up to 15 points for markers
                elif hasattr(node.func, 'attr') and node.func.attr == 'PolyLine':
                    points += 10
        
        return min(points, 40)  # Cap at 40 points
    except:
        return 0

def grade_assignment(code_str):
    """Main grading function"""
    total = 0
    
    # Code Structure and Implementation (30 points)
    total += check_imports(code_str)  # 5 points
    total += check_coordinates(code_str)  # 5 points
    
    try:
        exec(code_str)
        total += 10  # Code runs without errors
    except:
        pass
    
    # Code efficiency (simple check - could be improved)
    if len(code_str.split('\n')) < 50:
        total += 10
    elif len(code_str.split('\n')) < 100:
        total += 5
    
    # Map Visualization (40 points)
    total += check_map_visualization(code_str)
    
    # Distance Calculations (30 points)
    total += check_distance_calculations(code_str)
    
    return min(round(total), 100)  # Ensure total doesn't exceed 100

def load_or_create_grades_file():
    """Create or load the grades CSV file"""
    grades_file = Path("grades/data_submission.csv")
    grades_file.parent.mkdir(exist_ok=True)
    if not grades_file.exists():
        df = pd.DataFrame(columns=['name', 'student_id', 'total', 'week1'])
        df.to_csv(grades_file, index=False)
    return grades_file

def save_grade(name, student_id, total_grade):
    """Save grade to CSV file"""
    grades_file = load_or_create_grades_file()
    df = pd.read_csv(grades_file)
    if ((df['name'] == name) & (df['student_id'] == student_id)).any():
        df.loc[(df['name'] == name) & (df['student_id'] == student_id), 'week1'] = total_grade
        df.loc[(df['name'] == name) & (df['student_id'] == student_id), 'total'] = total_grade
    else:
        new_row = pd.DataFrame({
            'name': [name],
            'student_id': [student_id],
            'total': [total_grade],
            'week1': [total_grade]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(grades_file, index=False)

def extract_folium_map(namespace):
    """Extract Folium map object from namespace if it exists"""
    for obj in namespace.values():
        if isinstance(obj, folium.Map):
            return obj
    return None

def main():
    st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")

    # Student Information
    st.header("Student Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")

    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        **Objective:** Create a Python script to plot three geographical coordinates on a map and calculate distances between points.
        
        **Required Libraries:**
        - geopy for distance calculations
        - folium for mapping
        
        **Coordinates:**
        - Point 1: (36.325735, 43.928414)
        - Point 2: (36.393432, 44.586781)
        - Point 3: (36.660477, 43.840174)
        
        **Requirements:**
        1. Plot all three points on an interactive map
        2. Calculate distances between each pair of points in kilometers
        """)

    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Paste your code here", height=300)

    col1, col2 = st.columns(2)

    # Run Code Button
    if col1.button("Run Code"):
        if code.strip():
            # Create a temporary file to save the map
            temp_html = "temp_map.html"
            namespace = {}
            try:
                # Add display function to namespace
                namespace['display'] = lambda x: None  # Mock display function
                
                # Execute student code
                exec(code, namespace)
                st.success("Code executed successfully!")
                
                # Find and save the map
                folium_map = extract_folium_map(namespace)
                if folium_map:
                    folium_map.save(temp_html)
                    with open(temp_html, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    html(html_content, height=500)
                    # Clean up
                    import os
                    if os.path.exists(temp_html):
                        os.remove(temp_html)
                        
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
        else:
            st.warning("Please enter code before running")

    # Submit Assignment Button
    if col2.button("Submit Assignment"):
        if not all([name, email, student_id, code]):
            st.error("Please fill in all fields before submitting")
        else:
            try:
                # Grade the submission
                total_grade = grade_assignment(code)
                
                # Save grade to CSV
                save_grade(name, student_id, total_grade)
                
                st.success(f"Assignment submitted successfully! Total Grade: {total_grade}/100")
            except Exception as e:
                st.error(f"Error during submission: {str(e)}")

if __name__ == "__main__":
    main()

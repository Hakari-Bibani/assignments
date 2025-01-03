import streamlit as st
import os
import sys
from io import StringIO
from subprocess import run

# Assignment details
def show_assignment_details():
    st.title("Week 1 - Mapping Coordinates and Calculating Distances in Python")
    with st.expander("Assignment Details"):
        st.write("""
        **Objective**: In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.

        **Task Requirements:**
        1. Plot the three coordinates on a map using Python libraries.
        2. Calculate the distances between the points using geopy.
        
        **Coordinates:**
        - Point 1: Latitude: 36.325735, Longitude: 43.928414
        - Point 2: Latitude: 36.393432, Longitude: 44.586781
        - Point 3: Latitude: 36.660477, Longitude: 43.840174
        
        **Python Libraries You Will Use:**
        - `geopy` for distance calculation.
        - `folium` for plotting the map.
        - `geopandas` (optional) for advanced mapping.

        **Expected Output:**
        1. A map showing the three coordinates.
        2. A text summary showing the calculated distances between:
            - Point 1 and Point 2
            - Point 2 and Point 3
            - Point 1 and Point 3
        """)

# Collecting student info
def collect_student_info():
    with st.form(key='student_info_form'):
        st.text_input("Full Name", key="full_name")
        st.text_input("Email", key="email")
        st.text_input("Student ID", key="student_id")
        submit_button = st.form_submit_button(label="Submit Info")
        return submit_button

# Code submission and execution
def code_submission():
    code = st.text_area("Paste your Python code here", height=400)
    if st.button("Run Code"):
        # Capturing output of the script execution
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            exec(code)
            output = sys.stdout.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout = old_stdout
        st.text_area("Output", value=output, height=200)
        
    if st.button("Submit Assignment"):
        st.write("Submitting your assignment...")
        # You can implement auto-grading and save the results here.

# Main function to display everything
def main():
    show_assignment_details()
    student_info_submitted = collect_student_info()
    if student_info_submitted:
        code_submission()

if __name__ == "__main__":
    main()

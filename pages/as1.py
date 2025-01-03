import streamlit as st
import subprocess
import sys
import pandas as pd
import os
from grade1 import calculate_grade

# Ensure the grades directory exists
if not os.path.exists("grades"):
    os.makedirs("grades")

# Streamlit app title
st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")

# Student information input
st.header("Student Information")
full_name = st.text_input("Full Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID")

# Assignment details
st.header("Assignment Details")
with st.expander("View Assignment Instructions"):
    st.markdown("""
    **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**

    **Objective:**  
    In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.

    **Task Requirements:**
    1. **Plot the Three Coordinates on a Map:**
       - Use Python libraries to plot the points on a map.
       - The map should visually display the exact locations of the coordinates.
    2. **Calculate the Distance Between Each Pair of Points:**
       - Calculate the distances between the three points in **kilometers**.

    **Coordinates:**
    - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
    - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
    - **Point 3:** Latitude: 36.660477, Longitude: 43.840174

    **Python Libraries You Will Use:**
    - **geopy** for calculating distances.
    - **folium** for plotting points on an interactive map.
    - **geopandas** (optional) for advanced map rendering.

    **Expected Output:**
    1. A **map** showing the three coordinates.
    2. A **text summary** showing the calculated distances (in kilometers) between:
       - Point 1 and Point 2.
       - Point 2 and Point 3.
       - Point 1 and Point 3.
    """)

# Code submission
st.header("Code Submission")
student_code = st.text_area("Paste your Python code here", height=300)

# Run Code button
if st.button("Run Code"):
    if not student_code.strip():
        st.error("Please paste your code before running.")
    else:
        try:
            # Execute the student's code
            exec(student_code)
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"Error executing code: {e}")

# Submit Assignment button
if st.button("Submit Assignment"):
    if not full_name or not email or not student_id:
        st.error("Please fill in all student information fields.")
    elif not student_code.strip():
        st.error("Please paste your code before submitting.")
    else:
        # Calculate the grade
        grade = calculate_grade(student_code)

        # Save the grade and student information
        data = {
            "Full name": [full_name],
            "Email": [email],
            "Student ID": [student_id],
            "assignment1": [grade],
            "total": [grade]  # Assuming this is the first assignment
        }
        df = pd.DataFrame(data)

        # Append to the CSV file
        if not os.path.exists("grades/data_submission.csv"):
            df.to_csv("grades/data_submission.csv", index=False)
        else:
            existing_df = pd.read_csv("grades/data_submission.csv")
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv("grades/data_submission.csv", index=False)

        st.success(f"Assignment submitted successfully! Your grade is: {grade}/100")

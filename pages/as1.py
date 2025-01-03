import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
import os

# Page title
st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")

# Student information form
st.header("Student Information")
full_name = st.text_input("Full Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID")

# Assignment details in an accordion
with st.expander("Assignment Details"):
    st.markdown("""
    **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**

    **Objective:**  
    In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.

    **Task Requirements:**  
    1. Plot the Three Coordinates on a Map:  
       - Use Python libraries to plot the points on a map.  
       - The map should visually display the exact locations of the coordinates.  
    2. Calculate the Distance Between Each Pair of Points:  
       - Calculate the distances between the three points in kilometers.  

    **Coordinates:**  
    - Point 1: Latitude: 36.325735, Longitude: 43.928414  
    - Point 2: Latitude: 36.393432, Longitude: 44.586781  
    - Point 3: Latitude: 36.660477, Longitude: 43.840174  

    **Expected Output:**  
    1. A map showing the three coordinates.  
    2. A text summary showing the calculated distances (in kilometers) between:  
       - Point 1 and Point 2.  
       - Point 2 and Point 3.  
       - Point 1 and Point 3.  
    """)

# Code submission
st.header("Code Submission")
student_code = st.text_area("Paste your Python script here (copy from Google Colab):", height=300)

# Run code button
if st.button("Run Code"):
    if not full_name or not email or not student_id:
        st.error("Please fill in your full name, email, and student ID before running the code.")
    else:
        try:
            # Execute the student's code
            exec(student_code)

            # Display the map
            st.header("Map Visualization")
            if 'map' in locals():
                folium_static(map)  # Display the Folium map
            else:
                st.error("No map object found in the script. Ensure you create a Folium map and assign it to the variable `map`.")

            # Display the distances
            st.header("Distance Calculations")
            if 'distances' in locals():
                st.write(f"Distance between Point 1 and Point 2: {distances[0]:.2f} km")
                st.write(f"Distance between Point 2 and Point 3: {distances[1]:.2f} km")
                st.write(f"Distance between Point 1 and Point 3: {distances[2]:.2f} km")
            else:
                st.error("No distances found. Ensure you calculate the distances and store them in a list called `distances`.")

        except Exception as e:
            st.error(f"An error occurred while running your code: {e}")

# Submit assignment button
if st.button("Submit Assignment"):
    if not full_name or not email or not student_id:
        st.error("Please fill in your full name, email, and student ID before submitting.")
    else:
        try:
            # Grade the assignment
            from grade1 import grade_assignment
            grade = grade_assignment(student_code)

            # Save the grade to the CSV file
            grades_file = "grades/data_submission.csv"
            if not os.path.exists(grades_file):
                df = pd.DataFrame(columns=["Full Name", "Email", "Student ID", "Assignment1"])
            else:
                df = pd.read_csv(grades_file)

            # Add or update the student's grade
            df.loc[df["Student ID"] == student_id, ["Full Name", "Email", "Student ID", "Assignment1"]] = [full_name, email, student_id, grade]
            df.to_csv(grades_file, index=False)

            st.success(f"Assignment submitted successfully! Your grade is: {grade}/100")
        except Exception as e:
            st.error(f"An error occurred while grading your assignment: {e}")

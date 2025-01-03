import streamlit as st
import folium
from geopy.distance import geodesic
from io import StringIO
import pandas as pd
import os
from grades.grade1 import calculate_grade  # Updated import statement

# Define the coordinates
COORDINATES = {
    "Point 1": (36.325735, 43.928414),
    "Point 2": (36.393432, 44.586781),
    "Point 3": (36.660477, 43.840174),
}

# Streamlit app layout
st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")

# Student information input
st.sidebar.header("Student Information")
full_name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
student_id = st.sidebar.text_input("Student ID")

# Assignment details
with st.expander("Assignment Details"):
    st.markdown("""
    **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**

    **Objective:** Plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.

    **Task Requirements:**
    1. Plot the three coordinates on a map using `folium`.
    2. Calculate the distances between the points using `geopy`.

    **Coordinates:**
    - Point 1: Latitude: 36.325735, Longitude: 43.928414
    - Point 2: Latitude: 36.393432, Longitude: 44.586781
    - Point 3: Latitude: 36.660477, Longitude: 43.840174

    **Expected Output:**
    - A map showing the three coordinates.
    - A text summary of the calculated distances between the points.
    """)

# Code submission
st.header("Code Submission")
code_input = st.text_area("Paste your Python code here", height=300)

# Run code button
if st.button("Run Code"):
    if not code_input.strip():
        st.error("Please paste your code before running.")
    else:
        try:
            # Capture the output of the code
            output = StringIO()
            exec(code_input, {"COORDINATES": COORDINATES, "geodesic": geodesic, "folium": folium}, {"output": output})
            st.success("Code executed successfully!")

            # Display the map and distances
            st.subheader("Map Visualization")
            st.write(output.getvalue())

            # Grade the submission
            grade = calculate_grade(code_input)
            st.subheader("Grading Result")
            st.write(f"Your grade for this assignment is: {grade}/100")

            # Save the grade to CSV
            if full_name and student_id:
                save_grade(full_name, email, student_id, grade)
                st.success("Grade saved successfully!")
            else:
                st.error("Please fill in your full name and student ID to save your grade.")
        except Exception as e:
            st.error(f"Error executing code: {e}")

# Function to save grades to CSV
def save_grade(full_name, email, student_id, grade):
    data = {
        "Full name": [full_name],
        "Email": [email],
        "Student ID": [student_id],
        "assignment1": [grade],
    }
    df = pd.DataFrame(data)

    # Save to CSV
    os.makedirs("grades", exist_ok=True)
    if not os.path.exists("grades/data_submission.csv"):
        df.to_csv("grades/data_submission.csv", index=False)
    else:
        existing_df = pd.read_csv("grades/data_submission.csv")
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv("grades/data_submission.csv", index=False)

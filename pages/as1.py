import streamlit as st
import pandas as pd
import os
import sys
from streamlit_folium import st_folium  # For rendering Folium maps in Streamlit

# Add the 'grades' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../grades')))

# Now import grade_assignment
from grade1 import grade_assignment

# Page configuration
st.set_page_config(page_title="Assignment 1", layout="wide")

# Title and instructions
st.title("Week 1 – Mapping Coordinates and Calculating Distances in Python")
st.write("""
**Objective:** Plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.
""")

# Student information form
with st.form("student_info"):
    st.subheader("Student Information")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    submitted_info = st.form_submit_button("Submit Information")

# Assignment details in an accordion
with st.expander("Assignment Details"):
    st.write("""
    **Task Requirements:**
    1. Plot the Three Coordinates on a Map:
        - Use Python libraries to plot the points on a map.
        - The map should display the exact locations of the coordinates.
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

# Code submission and execution
st.subheader("Code Submission")
student_code = st.text_area("Paste your Python code here (copy from Google Colab):", height=300)
run_code = st.button("Run Code")

if run_code and student_code:
    try:
        # Preprocess the student's code
        # Remove or replace HTML-related code
        student_code = student_code.replace(
            "from folium import HTML",
            ""
        )
        student_code = student_code.replace(
            "from IPython.display import display",
            "from streamlit_folium import st_folium"
        )
        student_code = student_code.replace("display(", "st_folium(")
        student_code = student_code.replace("print(", "st.write(")

        # Execute the modified student code
        exec(student_code, globals())
        st.success("Code executed successfully!")
    except Exception as e:
        st.error(f"Error executing code: {e}")

# Submit assignment for grading
if st.button("Submit Assignment"):
    if not full_name or not email or not student_id:
        st.error("Please fill in your full name, email, and student ID.")
    else:
        # Grade the assignment
        grade = grade_assignment(student_code)
        
        # Save the grade to data_submission.csv
        grades_path = os.path.join("grades", "data_submission.csv")
        if not os.path.exists(grades_path):
            df = pd.DataFrame(columns=["Full name", "Student ID", "Email", "assignment1"])
        else:
            df = pd.read_csv(grades_path)
        
        # Update or add the student's grade
        if student_id in df["Student ID"].values:
            df.loc[df["Student ID"] == student_id, "assignment1"] = grade
        else:
            new_row = {"Full name": full_name, "Student ID": student_id, "Email": email, "assignment1": grade}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        df.to_csv(grades_path, index=False)
        st.success(f"Assignment submitted successfully! Your grade: {grade}/100")

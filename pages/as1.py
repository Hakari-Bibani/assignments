import streamlit as st
import folium
from folium.plugins import Marker
from geopy.distance import geodesic
import pandas as pd
import os

# Page configuration
st.set_page_config(page_title="Week 1 Assignment", layout="wide")
st.title("Week 1 – Mapping Coordinates and Calculating Distances in Python")

# Student information input
st.sidebar.header("Student Information")
full_name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
student_id = st.sidebar.text_input("Student ID")

# Assignment details in an accordion
with st.expander("Assignment Details"):
    st.markdown("""
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
student_code = st.text_area("Paste your Python script here (from Google Colab):", height=300)

# Run code button
if st.button("Run Code"):
    if not student_code:
        st.error("Please paste your code before running.")
    else:
        try:
            # Execute the student's code
            exec(student_code)
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"Error executing code: {e}")

# Submit assignment button
if st.button("Submit Assignment"):
    if not full_name or not email or not student_id:
        st.error("Please fill in all student information fields.")
    else:
        # Grade the assignment
        from grade1 import grade_assignment
        grade = grade_assignment(student_code)
        
        # Save the grade to CSV
        if not os.path.exists("grades/data_submission.csv"):
            df = pd.DataFrame(columns=["Full Name", "Email", "Student ID", "Assignment1"])
        else:
            df = pd.read_csv("grades/data_submission.csv")
        
        new_row = {"Full Name": full_name, "Email": email, "Student ID": student_id, "Assignment1": grade}
        df = df.append(new_row, ignore_index=True)
        df.to_csv("grades/data_submission.csv", index=False)
        
        st.success(f"Assignment submitted successfully! Your grade: {grade}/100")

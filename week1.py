import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import folium_static
import os

def run():
    st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")
    
    # Student Information Section
    st.subheader("Student Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    
    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        ## Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python
        
        ### Objective
        Write a Python script to plot three geographical coordinates on a map and calculate 
        the distance between each pair of points in kilometers.
        
        ### Task Requirements
        1. **Plot the Three Coordinates on a Map:**
           - Plot three locations in the Kurdistan Region
           - Use Python libraries to visualize the points
           
        2. **Calculate the Distance Between Each Pair of Points:**
           - Calculate distances in kilometers between:
             - Point 1 and Point 2
             - Point 2 and Point 3
             - Point 1 and Point 3
        
        ### Coordinates:
        - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
        - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
        - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
        
        ### Required Libraries:
        - geopy for distance calculations
        - folium for map visualization
        - geopandas (optional)
        """)
    
    # Code Submission Section
    st.subheader("Code Submission")
    code = st.text_area("Paste your code here:", height=300)
    
    # Run Code Button
    if st.button("Run Code"):
        if code.strip():
            try:
                # Create a temporary Python file with the submitted code
                with open("temp_submission.py", "w") as f:
                    f.write(code)
                
                # Execute the code and capture output
                exec(code, globals())
                
                st.success("Code executed successfully!")
                
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
        else:
            st.warning("Please enter code before running.")
    
    # Submit Assignment Button
    if st.button("Submit Assignment"):
        if not all([name, email, student_id, code]):
            st.error("Please fill in all fields before submitting.")
            return
            
        # Save submission to CSV
        submission_data = {
            'name': name,
            'student_id': student_id,
            'email': email,
            'week': 1,
            'code': code,
            'total': 0  # Will be updated by grading script
        }
        
        # Create grades directory if it doesn't exist
        os.makedirs('grades', exist_ok=True)
        
        # Save or append to CSV
        df = pd.DataFrame([submission_data])
        if os.path.exists('grades/data_submission.csv'):
            df.to_csv('grades/data_submission.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('grades/data_submission.csv', index=False)
        
        # Run grading script
        import grade1
        grade = grade1.grade()
        st.success(f"Assignment submitted successfully! Grade: {grade}/100")

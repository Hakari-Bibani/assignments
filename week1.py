import streamlit as st
import pandas as pd
import os
from grade1 import grade_assignment
import sys
import io

def main():
    st.title("Week 1 Assignment")
    
    # Student Information
    st.header("Student Information")
    name = st.text_input("Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    
    # Assignment Details
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        ## Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python
        
        **Objective:** In this assignment, you will write a Python script to plot three geographical coordinates 
        on a map and calculate the distance between each pair of points in kilometers.
        
        ### Task Requirements:
        1. **Plot the Three Coordinates on a Map:**
           - The coordinates represent three locations in the Kurdistan Region
           - Use Python libraries to plot these points on a map
           - The map should visually display the exact locations of the coordinates
        
        2. **Calculate the Distance Between Each Pair of Points:**
           - Calculate the distances between the three points in **kilometers**
           - Specifically, calculate:
             - The distance between **Point 1** and **Point 2**
             - The distance between **Point 2** and **Point 3**
             - The distance between **Point 1** and **Point 3**
        
        ### Coordinates:
        - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
        - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
        - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
        
        ### Python Libraries You Will Use:
        - **geopy** for calculating the distance between two coordinates
        - **folium** for plotting the points on an interactive map
        - **geopandas** (optional) for advanced map rendering
        """)
    
    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Paste your code here:", height=300)
    
    # Run Code Button
    if st.button("Run Code"):
        if code.strip():
            # Capture stdout to display print statements
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            
            try:
                # Create a local namespace
                local_dict = {}
                # Execute the code
                exec(code, globals(), local_dict)
                
                # Get the captured output
                output = mystdout.getvalue()
                st.success("Code executed successfully!")
                if output:
                    st.text("Output:")
                    st.code(output)
                
                # Look for and display any map object
                if 'map' in local_dict:
                    map_obj = local_dict['map']
                    # Save map to HTML and display
                    map_obj.save('temp_map.html')
                    with open('temp_map.html', 'r') as f:
                        html_data = f.read()
                    st.components.v1.html(html_data, height=500)
                    os.remove('temp_map.html')
                
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
            
            finally:
                sys.stdout = old_stdout
        else:
            st.warning("Please enter some code to run")
    
    # Submit Assignment Button
    if st.button("Submit Assignment"):
        if not all([name, email, student_id, code]):
            st.error("Please fill in all fields before submitting")
            return
        
        # Grade the assignment
        grade, feedback = grade_assignment(code)
        
        # Display results
        st.success(f"Total Grade: {grade}/100")
        st.write("Feedback:", feedback)
        
        # Save to CSV
        csv_path = "grades/data_submission.csv"
        os.makedirs("grades", exist_ok=True)
        
        # Create or update the CSV file
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Name', 'Email', 'Student_ID', 'Total', 'Week1'])
        
        # Update or append new submission
        new_data = {
            'Name': name,
            'Email': email,
            'Student_ID': student_id,
            'Total': grade,
            'Week1': grade
        }
        
        # Check if student already exists
        mask = df['Student_ID'] == student_id
        if mask.any():
            # Update existing record
            for col, value in new_data.items():
                df.loc[mask, col] = value
        else:
            # Append new record
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        
        # Save to CSV
        df.to_csv(csv_path, index=False)
        st.success("Assignment submitted successfully!")

if __name__ == "__main__":
    main()

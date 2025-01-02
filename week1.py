import streamlit as st
import os
import pandas as pd
from grade1 import grade_submission
import ast
import sys
from io import StringIO
import traceback

# Set page config
st.set_page_config(page_title="Week 1 - Mapping Coordinates Assignment", layout="wide")

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create grades directory if it doesn't exist
create_directory_if_not_exists("grades")

def save_submission(name, student_id, total_grade, week_num=1):
    """Save submission details to CSV"""
    filename = "grades/data_submission.csv"
    data = {
        'name': [name],
        'student_id': [student_id],
        'total': [total_grade],
        f'week{week_num}': [total_grade]
    }
    
    new_df = pd.DataFrame(data)
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        # Update if student already exists, otherwise append
        if ((df['name'] == name) & (df['student_id'] == student_id)).any():
            idx = df[(df['name'] == name) & (df['student_id'] == student_id)].index
            df.loc[idx, ['total', f'week{week_num}']] = total_grade
        else:
            df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = new_df
        
    df.to_csv(filename, index=False)

def run_student_code(code_string):
    """Execute student code and capture output"""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        exec(code_string)
        sys.stdout = old_stdout
        return redirected_output.getvalue(), None
    except Exception as e:
        sys.stdout = old_stdout
        return None, str(e)

def main():
    st.title("Week 1 - Mapping Coordinates and Distance Calculation")
    
    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        ### Objective
        Write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.
        
        ### Task Requirements
        1. **Plot the Three Coordinates on a Map:**
           - Plot coordinates representing three locations in the Kurdistan Region
           - Use Python libraries to display these points on a map
           - Show exact locations of the coordinates
           
        2. **Calculate the Distance Between Each Pair of Points:**
           - Calculate distances between the three points in kilometers
           - Required calculations:
             - Distance between Point 1 and Point 2
             - Distance between Point 2 and Point 3
             - Distance between Point 1 and Point 3
        
        ### Coordinates
        - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
        - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
        - **Point 3:** Latitude: 36.660477, Longitude: 43.840174
        
        ### Required Libraries
        - **geopy** for distance calculations
        - **folium** for interactive map plotting
        - **geopandas** (optional) for advanced mapping
        """)

    # Student Information
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Full Name")
    with col2:
        student_id = st.text_input("Student ID")

    # Code Submission
    st.subheader("Code Submission")
    code_input = st.text_area("Paste your code here:", height=300)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Run Code"):
            if code_input.strip():
                output, error = run_student_code(code_input)
                if error:
                    st.error(f"Error in code execution:\n{error}")
                else:
                    st.success("Code executed successfully!")
                    st.code(output)
            else:
                st.warning("Please enter code before running.")

    with col2:
        if st.button("Submit Assignment"):
            if not all([student_name, student_id, code_input]):
                st.error("Please fill in all required fields (name, student ID, and code).")
                return
            
            # Grade the submission
            total_grade, feedback = grade_submission(code_input)
            
            # Save the grade
            save_submission(student_name, student_id, total_grade)
            
            # Display results
            st.success(f"Total Grade: {total_grade}/100")
            st.write("Feedback:")
            st.write(feedback)

if __name__ == "__main__":
    main()

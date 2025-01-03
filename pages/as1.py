# as1.py
import streamlit as st
import pandas as pd
import sys
import io
from pathlib import Path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'grades'))
from grade1 import grade_assignment

def main():
    st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")
    
    # Student Information
    st.subheader("Student Information")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    
    # Assignment Details in Accordion
    with st.expander("Assignment Details", expanded=True):
        st.markdown("""
        **Objective:** Write a Python script to plot three geographical coordinates on a map and calculate 
        the distance between each pair of points in kilometers.
        
        **Coordinates:**
        - Point 1: Latitude: 36.325735, Longitude: 43.928414
        - Point 2: Latitude: 36.393432, Longitude: 44.586781
        - Point 3: Latitude: 36.660477, Longitude: 43.840174
        
        **Required Libraries:**
        - geopy for distance calculations
        - folium for map visualization
        - geopandas (optional) for advanced mapping
        
        **Expected Output:**
        1. Interactive map showing the three points
        2. Distance calculations between all points
        """)
    
    # Code Submission
    st.subheader("Code Submission")
    user_code = st.text_area("Enter your code here:", height=300)
    
    # Run Code Button
    if st.button("Run Code"):
        if user_code.strip():
            # Capture stdout to display print statements
            old_stdout = sys.stdout
            redirected_output = io.StringIO()
            sys.stdout = redirected_output
            
            try:
                # Execute user code
                exec(user_code)
                sys.stdout = old_stdout
                output = redirected_output.getvalue()
                
                # Display output
                if output:
                    st.text("Output:")
                    st.text(output)
                
                # Look for map object in locals
                local_vars = locals()
                if 'm' in local_vars and 'folium' in user_code:
                    st.components.v1.html(local_vars['m']._repr_html_(), height=500)
                
            except Exception as e:
                sys.stdout = old_stdout
                st.error(f"Error executing code: {str(e)}")
    
    # Submit Assignment Button
    if st.button("Submit Assignment"):
        if not all([full_name, email, student_id, user_code]):
            st.error("Please fill in all fields before submitting.")
            return
            
        # Grade the submission
        grade, feedback = grade_assignment(user_code)
        
        # Display results
        st.subheader("Grading Results")
        st.write(f"Total Grade: {grade}/100")
        st.write("Feedback:", feedback)
        
        # Save to CSV
        csv_path = Path("grades/data_submission.csv")
        try:
            if csv_path.exists():
                df = pd.read_csv(csv_path)
            else:
                # Create DataFrame with all assignment columns
                columns = ['full_name', 'student_id'] + [f'assignment{i}' for i in range(1, 16)] + \
                         [f'quiz{i}' for i in range(1, 11)] + ['total']
                df = pd.DataFrame(columns=columns)
            
            # Update or add new row
            new_row = {col: 0 for col in df.columns}  # Initialize with zeros
            new_row.update({
                'full_name': full_name,
                'student_id': student_id,
                'assignment1': grade
            })
            
            # Update if student exists, else append
            mask = (df['student_id'] == student_id)
            if mask.any():
                df.loc[mask, 'assignment1'] = grade
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Calculate total
            numeric_cols = [col for col in df.columns if col not in ['full_name', 'student_id']]
            df['total'] = df[numeric_cols].sum(axis=1)
            
            # Save to CSV
            df.to_csv(csv_path, index=False)
            st.success("Grade saved successfully!")
            
        except Exception as e:
            st.error(f"Error saving grade: {str(e)}")

if __name__ == "__main__":
    main()

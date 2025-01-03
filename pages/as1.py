# as1.py
import streamlit as st
import pandas as pd
import os
import base64
import folium

def run_assignment():
    st.title("Week 1 Assignment - Mapping Coordinates")
    
    # Student Information
    with st.form("student_info"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        student_id = st.text_input("Student ID")
        
        # Assignment Details in Accordion
        with st.expander("Assignment Details", expanded=True):
            st.markdown("""
            **Objective:** Plot geographical coordinates and calculate distances in Python
            
            **Coordinates:**
            - Point 1: 36.325735, 43.928414
            - Point 2: 36.393432, 44.586781
            - Point 3: 36.660477, 43.840174
            
            **Required Libraries:**
            - geopy for distance calculations
            - folium for mapping
            """)
        
        # Code Input
        code = st.text_area("Paste your code here:", height=300)
        
        submitted = st.form_submit_button("Submit Assignment")

    if st.button("Run Code"):
        if code:
            try:
                # Capture the map output
                namespace = {}
                exec(code, namespace)
                
                # If a map was created, save it as HTML and display it
                if 'm' in namespace and isinstance(namespace['m'], folium.Map):
                    map_html = namespace['m']._repr_html_()
                    st.components.v1.html(map_html, height=500)
                
                st.success("Code executed successfully!")
            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
    
    if submitted and full_name and email and student_id and code:
        try:
            # Calculate grade
            from grade1 import grade_assignment
            grade = grade_assignment(code)
            
            # Create grades directory if it doesn't exist
            os.makedirs('grades', exist_ok=True)
            
            # Create or load CSV file
            csv_path = "grades/data_submission.csv"
            if not os.path.exists(csv_path):
                df = pd.DataFrame(columns=['full_name', 'student_id', 'email'] + 
                                [f'assignment{i}' for i in range(1, 16)] +
                                [f'quiz{i}' for i in range(1, 11)] +
                                ['total'])
            else:
                df = pd.read_csv(csv_path)
            
            # Update or add new student record
            new_data = {
                'full_name': full_name,
                'student_id': student_id,
                'email': email,
                'assignment1': grade
            }
            
            if student_id in df['student_id'].values:
                df.loc[df['student_id'] == student_id, 'assignment1'] = grade
            else:
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            
            df.to_csv(csv_path, index=False)
            st.success(f"Assignment submitted! Grade: {grade}/100")
        except Exception as e:
            st.error(f"Error during submission: {str(e)}")
    elif submitted:
        st.warning("Please fill in all required fields")

if __name__ == "__main__":
    run_assignment()

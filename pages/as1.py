import os
import streamlit as st
import pandas as pd

# Define the absolute path to the repository root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Adjust based on your repo structure
GRADES_DIR = os.path.join(REPO_ROOT, 'grades')
FILE_PATH = os.path.join(GRADES_DIR, 'data_submission.csv')

# Ensure the 'grades' directory exists
os.makedirs(GRADES_DIR, exist_ok=True)

with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in both your Name and Email before submitting.")
        elif 'map_obj' not in st.session_state or 'distances' not in st.session_state:
            st.error("Please run your code and generate the map before submitting.")
        else:
            try:
                # Grade the submission
                from grades.grade1 import grade_submission
                score, breakdown = grade_submission(code)

                # Prepare submission dictionary
                submission = {
                    'fullname': name.strip(),
                    'email': email.strip(),
                    'studentID': student_id.strip() if student_id else 'N/A',
                    'assigment1': score
                }

                # Load existing data or create a new DataFrame
                try:
                    # Try reading the existing CSV
                    df = pd.read_csv(FILE_PATH)
                except FileNotFoundError:
                    # Create a new DataFrame with all required columns
                    columns = [
                        'fullname', 'email', 'studentID', 'assigment1', 'assigment2', 'assigment3', 
                        'assigment4', 'assigment5', 'assigment6', 'assigment7', 'assigment8', 
                        'assigment9', 'assigment10', 'assigment11', 'assigment12', 'assigment13', 
                        'assigment14', 'assigment15', 'quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 
                        'quiz6', 'quiz7', 'quiz8', 'quiz9', 'quiz10', 'total'
                    ]
                    df = pd.DataFrame(columns=columns)

                # Debug: Print the file path and DataFrame before update
                st.write(f"File Path: {FILE_PATH}")
                st.write("DataFrame Before Update:", df)

                # Check if the student already exists in the DataFrame
                if submission['fullname'] in df['fullname'].values:
                    # Update existing student's data
                    df.loc[df['fullname'] == submission['fullname'], ['email', 'studentID', 'assigment1']] = \
                        [submission['email'], submission['studentID'], submission['assigment1']]
                else:
                    # Add new student data
                    new_row = {col: submission.get(col, None) for col in df.columns}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

                # Recalculate the 'total' column as the sum of all assignment and quiz columns
                assignment_columns = [col for col in df.columns if col.startswith('assigment')]
                quiz_columns = [col for col in df.columns if col.startswith('quiz')]
                df['total'] = df[assignment_columns + quiz_columns].sum(axis=1)

                # Debug: Print DataFrame after update
                st.write("DataFrame After Update:", df)

                # Save the updated DataFrame back to the CSV file
                df.to_csv(FILE_PATH, index=False)

                # Confirm successful submission
                st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")
                st.error("Please check the 'grades' directory and file permissions.")

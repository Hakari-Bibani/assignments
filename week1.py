import streamlit as st
import pandas as pd
from pathlib import Path

def run():
    st.title("Week 1: Introduction to Python")
    
    # Student information
    st.subheader("Student Information")
    student_name = st.text_input("Name")
    student_id = st.text_input("Student ID")
    
    # Assignment questions
    st.subheader("Assignment Questions")
    
    # Question 1
    st.markdown("#### Question 1")
    st.write("What is Python's primary use case?")
    q1_answer = st.text_area("Your Answer", key="q1")
    
    # Question 2
    st.markdown("#### Question 2")
    st.write("Write a Python function that prints 'Hello, World!'")
    q2_answer = st.text_area("Your Answer", key="q2")
    
    # Submit button
    if st.button("Submit Assignment"):
        if not student_name or not student_id:
            st.error("Please fill in your name and student ID")
            return
            
        # Save submission
        submission = {
            'student_name': student_name,
            'student_id': student_id,
            'q1_answer': q1_answer,
            'q2_answer': q2_answer,
            'week': 1,
            'timestamp': pd.Timestamp.now()
        }
        
        # Save to CSV
        save_submission(submission)
        
        # Run grading
        import grade1
        grade1.grade_submission(submission)
        
        st.success("Assignment submitted successfully!")

def save_submission(submission):
    # Create grades directory if it doesn't exist
    Path('grades').mkdir(exist_ok=True)
    
    # Create or load existing submissions
    csv_path = 'grades/data_submission.csv'
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame()
    
    # Append new submission
    new_df = pd.concat([df, pd.DataFrame([submission])], ignore_index=True)
    new_df.to_csv(csv_path, index=False)

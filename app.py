# app.py
import streamlit as st
import pandas as pd
from style import apply_style
import importlib

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'
if 'submission_data' not in st.session_state:
    st.session_state.submission_data = {}

# Apply custom styling
apply_style()

def save_submission(data):
    """Save submission data to CSV"""
    df = pd.DataFrame([data])
    try:
        existing_df = pd.read_csv('grades/data_submission.csv')
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df
    updated_df.to_csv('grades/data_submission.csv', index=False)

def create_assignment_page(week_num):
    st.title(f"Week {week_num} Assignment")
    
    # Student Information
    st.header("Student Information")
    name = st.text_input("Name", key=f"name_week_{week_num}")
    email = st.text_input("Email", key=f"email_week_{week_num}")
    student_id = st.text_input("Student ID (Optional)", key=f"id_week_{week_num}")
    
    # Assignment Content
    st.header("Assignment")
    try:
        week_module = importlib.import_module(f'week{week_num}')
        week_module.show_content()
    except ImportError:
        st.error(f"Week {week_num} content not found.")
        return
    
    # Code Submission
    st.header("Code Submission")
    code = st.text_area("Enter your code here:", height=200, key=f"code_week_{week_num}")
    
    # Run Code Button
    if st.button("Run Code", key=f"run_week_{week_num}"):
        try:
            exec(code)
        except Exception as e:
            st.error(f"Error executing code: {str(e)}")
    
    # Submit Button
    if st.button("Submit Assignment", key=f"submit_week_{week_num}"):
        if not name or not email:
            st.error("Please fill in required fields (Name and Email)")
            return
        
        # Grade the submission
        try:
            grade_module = importlib.import_module(f'grade{week_num}')
            grade = grade_module.grade_submission(code)
            
            # Prepare submission data
            submission_data = {
                'Name': name,
                'Email': email,
                'Student ID': student_id,
            }
            
            # Initialize all week and quiz grades to 0
            for w in range(1, 16):
                submission_data[f'Week {w}'] = 0
            for q in range(1, 11):
                submission_data[f'Quiz {q}'] = 0
            
            # Update the specific week's grade
            submission_data[f'Week {week_num}'] = grade
            
            # Calculate total
            submission_data['Total'] = sum(
                submission_data[f'Week {w}'] for w in range(1, 16)
            ) + sum(
                submission_data[f'Quiz {q}'] for q in range(1, 11)
            )
            
            save_submission(submission_data)
            st.success(f"Assignment submitted successfully! Grade: {grade}")
            
        except Exception as e:
            st.error(f"Error grading submission: {str(e)}")

def create_quiz_page(quiz_num):
    st.title(f"Quiz {quiz_num}")
    
    # Student Information
    st.header("Student Information")
    name = st.text_input("Name", key=f"name_quiz_{quiz_num}")
    email = st.text_input("Email", key=f"email_quiz_{quiz_num}")
    student_id = st.text_input("Student ID (Optional)", key=f"id_quiz_{quiz_num}")
    
    # Quiz Content
    st.header("Quiz")
    try:
        quiz_module = importlib.import_module(f'quiz{quiz_num}')
        quiz_module.show_content()
    except ImportError:
        st.error(f"Quiz {quiz_num} content not found.")
        return
    
    # Answer Submission
    st.header("Your Answers")
    answers = st.text_area("Enter your answers here:", height=200, key=f"answers_quiz_{quiz_num}")
    
    # Submit Button
    if st.button("Submit Quiz", key=f"submit_quiz_{quiz_num}"):
        if not name or not email:
            st.error("Please fill in required fields (Name and Email)")
            return
        
        try:
            # Grade the quiz
            grade_module = importlib.import_module('gradequizes')
            grade = grade_module.grade_quiz(quiz_num, answers)
            
            # Prepare submission data
            submission_data = {
                'Name': name,
                'Email': email,
                'Student ID': student_id,
            }
            
            # Initialize all week and quiz grades to 0
            for w in range(1, 16):
                submission_data[f'Week {w}'] = 0
            for q in range(1, 11):
                submission_data[f'Quiz {q}'] = 0
            
            # Update the specific quiz's grade
            submission_data[f'Quiz {quiz_num}'] = grade
            
            # Calculate total
            submission_data['Total'] = sum(
                submission_data[f'Week {w}'] for w in range(1, 16)
            ) + sum(
                submission_data[f'Quiz {q}'] for q in range(1, 11)
            )
            
            save_submission(submission_data)
            st.success(f"Quiz submitted successfully! Grade: {grade}")
            
        except Exception as e:
            st.error(f"Error grading quiz: {str(e)}")

def main():
    st.set_page_config(page_title="ImpactHub", layout="wide")
    
    if st.session_state.current_page == 'main':
        st.title("ImpactHub")
        
        # Create two columns for Assignments and Quizzes
        col1, col2 = st.columns(2)
        
        # Assignments Column
        with col1:
            st.header("Assignments")
            for week in range(1, 16):
                if st.button(f"Week {week}", key=f"week_{week}"):
                    st.session_state.current_page = f'week_{week}'
                    st.experimental_rerun()
        
        # Quizzes Column
        with col2:
            st.header("Quizzes")
            for quiz in range(1, 11):
                if st.button(f"Quiz {quiz}", key=f"quiz_{quiz}"):
                    st.session_state.current_page = f'quiz_{quiz}'
                    st.experimental_rerun()
    
    else:
        # Add a return to main page button
        if st.button("← Back to Main Page"):
            st.session_state.current_page = 'main'
            st.experimental_rerun()
        
        # Handle week pages
        if st.session_state.current_page.startswith('week_'):
            week_num = int(st.session_state.current_page.split('_')[1])
            create_assignment_page(week_num)
        
        # Handle quiz pages
        elif st.session_state.current_page.startswith('quiz_'):
            quiz_num = int(st.session_state.current_page.split('_')[1])
            create_quiz_page(quiz_num)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import os
from style import set_page_style
import importlib

# Initialize the page
st.set_page_config(page_title="ImpactHub", layout="wide")
set_page_style()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

# Function to load or create submission data
def load_submission_data():
    csv_path = 'grades/data_submission.csv'
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Create empty DataFrame with all required columns
        columns = ['Name', 'Email', 'Student_ID', 'Total'] + \
                 [f'Week_{i}' for i in range(1, 16)] + \
                 [f'Quiz_{i}' for i in range(1, 11)]
        df = pd.DataFrame(columns=columns)
        os.makedirs('grades', exist_ok=True)
        df.to_csv(csv_path, index=False)
        return df

# Function to save submission
def save_submission(data):
    df = load_submission_data()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv('grades/data_submission.csv', index=False)

# Function to handle assignment submission
def handle_submission(week_num=None, quiz_num=None):
    name = st.session_state.get('name', '')
    email = st.session_state.get('email', '')
    student_id = st.session_state.get('student_id', '')
    code = st.session_state.get('code', '')
    
    if not name or not email or not code:
        st.error("Please fill in all required fields")
        return
    
    submission_data = {
        'Name': name,
        'Email': email,
        'Student_ID': student_id,
    }
    
    # Import appropriate grading module
    if week_num:
        grade_module = importlib.import_module(f'grade{week_num}')
        grade = grade_module.grade_assignment(code)
        submission_data[f'Week_{week_num}'] = grade
    elif quiz_num:
        grade_module = importlib.import_module('gradequizes')
        grade = grade_module.grade_quiz(quiz_num, code)
        submission_data[f'Quiz_{quiz_num}'] = grade
    
    # Calculate total
    submission_data['Total'] = grade  # You might want to modify this based on your grading scheme
    
    save_submission(submission_data)
    st.success("Assignment submitted successfully!")

# Main page content
def main_page():
    st.title("ImpactHub - Assignment Portal")
    
    # Create grid layout for cards
    col1, col2, col3 = st.columns(3)
    
    # Weeks
    for i in range(1, 16):
        with col1 if i % 3 == 1 else col2 if i % 3 == 2 else col3:
            if st.button(f"Week {i}", key=f"week_{i}", use_container_width=True):
                st.session_state.current_page = f'week_{i}'
                st.rerun()
    
    st.markdown("---")
    
    # Quizzes
    for i in range(1, 11):
        with col1 if i % 3 == 1 else col2 if i % 3 == 2 else col3:
            if st.button(f"Quiz {i}", key=f"quiz_{i}", use_container_width=True):
                st.session_state.current_page = f'quiz_{i}'
                st.rerun()

# Assignment/Quiz page content
def assignment_page(week_num=None, quiz_num=None):
    page_type = "Quiz" if quiz_num else "Week"
    num = quiz_num if quiz_num else week_num
    
    st.title(f"{page_type} {num}")
    
    # Back button
    if st.button("← Back to Main Page"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    # Student information
    st.subheader("Student Information")
    st.text_input("Name *", key="name")
    st.text_input("Email *", key="email")
    st.text_input("Student ID", key="student_id")
    
    # Assignment content
    st.subheader("Assignment Details")
    if quiz_num:
        quiz_module = importlib.import_module(f'quiz{quiz_num}')
        st.markdown(quiz_module.get_description())
    else:
        week_module = importlib.import_module(f'week{week_num}')
        st.markdown(week_module.get_description())
    
    # Code submission
    st.subheader("Code Submission")
    st.text_area("Enter your code here *", height=300, key="code")
    
    # Submit button
    if st.button("Submit Assignment"):
        handle_submission(week_num, quiz_num)

# Main app logic
if st.session_state.current_page == 'main':
    main_page()
else:
    page_type, num = st.session_state.current_page.split('_')
    if page_type == 'week':
        assignment_page(week_num=int(num))
    else:
        assignment_page(quiz_num=int(num))

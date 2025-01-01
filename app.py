import streamlit as st
import pandas as pd
import importlib
import os
from pathlib import Path
import sys
from style import app_style

# Setup page configuration
st.set_page_config(
    page_title="ImpactHub",
    page_icon="📚",
    layout="wide"
)

# Apply custom styling
app_style()

def load_module(module_name):
    """Dynamically import a module."""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Error loading module {module_name}: {str(e)}")
        return None

def save_submission(data):
    """Save submission data to CSV file."""
    csv_path = "grades/data_submission.csv"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Read existing data or create new DataFrame
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame()
    
    # Convert data to DataFrame and append
    new_data = pd.DataFrame([data])
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save to CSV
    df.to_csv(csv_path, index=False)

def calculate_total_grade(grades_dict):
    """Calculate total grade from individual assignments."""
    return sum(float(grade) for grade in grades_dict.values() if isinstance(grade, (int, float)))

def main():
    st.title("ImpactHub Learning Platform")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    pages = ["Main Page", "Week Assignments", "Quizzes"]
    selection = st.sidebar.radio("Go to", pages)
    
    if selection == "Main Page":
        st.header("Welcome to ImpactHub!")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Weekly Assignments")
            for week in range(1, 16):
                if st.button(f"Week {week}", key=f"week_{week}"):
                    st.session_state.page = f"week{week}"
                    st.session_state.current_week = week
                    st.experimental_rerun()
        
        with col2:
            st.subheader("Quizzes")
            for quiz in range(1, 11):
                if st.button(f"Quiz {quiz}", key=f"quiz_{quiz}"):
                    st.session_state.page = f"quiz{quiz}"
                    st.session_state.current_quiz = quiz
                    st.experimental_rerun()
    
    elif selection in ["Week Assignments", "Quizzes"]:
        # Student Information Form
        st.header("Student Information")
        name = st.text_input("Full Name", key="name")
        email = st.text_input("Email", key="email")
        student_id = st.text_input("Student ID (Optional)", key="student_id")
        
        if selection == "Week Assignments" and "current_week" in st.session_state:
            week_num = st.session_state.current_week
            week_module = load_module(f"week{week_num}")
            grade_module = load_module(f"grade{week_num}")
            
            if week_module and grade_module:
                st.header(f"Week {week_num} Assignment")
                
                # Display assignment description
                st.markdown(week_module.get_description())
                
                # Code submission
                code = st.text_area("Enter your code here:", height=300)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Run Code"):
                        try:
                            # Execute code in a safe environment
                            exec(code)
                        except Exception as e:
                            st.error(f"Error executing code: {str(e)}")
                
                with col2:
                    if st.button("Submit Assignment"):
                        if not name or not email:
                            st.error("Please fill in required fields (Name and Email)")
                        else:
                            # Grade the submission
                            grade = grade_module.grade_assignment(code)
                            
                            # Prepare submission data
                            submission_data = {
                                "Name": name,
                                "Email": email,
                                "Student_ID": student_id,
                                f"Week_{week_num}": grade
                            }
                            
                            # Save submission
                            save_submission(submission_data)
                            st.success(f"Assignment submitted! Grade: {grade}")
        
        elif selection == "Quizzes" and "current_quiz" in st.session_state:
            quiz_num = st.session_state.current_quiz
            quiz_module = load_module(f"quiz{quiz_num}")
            grade_module = load_module("gradequizes")
            
            if quiz_module and grade_module:
                st.header(f"Quiz {quiz_num}")
                
                # Display quiz questions and handle submissions
                answers = quiz_module.display_quiz()
                
                if st.button("Submit Quiz"):
                    if not name or not email:
                        st.error("Please fill in required fields (Name and Email)")
                    else:
                        # Grade the quiz
                        grade = grade_module.grade_quiz(quiz_num, answers)
                        
                        # Prepare submission data
                        submission_data = {
                            "Name": name,
                            "Email": email,
                            "Student_ID": student_id,
                            f"Quiz_{quiz_num}": grade
                        }
                        
                        # Save submission
                        save_submission(submission_data)
                        st.success(f"Quiz submitted! Grade: {grade}")

if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "main"
    main()

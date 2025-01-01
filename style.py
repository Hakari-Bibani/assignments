def get_style():
    return """
    <style>
    .card {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .card h3 {
        margin: 0 0 0.5rem 0;
        color: #1f1f1f;
    }
    
    .card a {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #ff4b4b;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        margin-top: 1rem;
    }
    </style>
    """

# Template for week#.py pages
def create_assignment_page(week_number):
    return f"""
import streamlit as st
import pandas as pd
from pathlib import Path
import grade{week_number} as grader

def main():
    st.title(f"Week {week_number} Assignment")
    
    with st.form(f"week_{week_number}_submission"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        student_id = st.text_input("Student ID")
        code = st.text_area("Code Submission")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Grade submission
            grade = grader.grade_submission(code)
            
            # Update grades CSV
            update_grades(name, email, student_id, week_number, grade)
            
            st.success(f"Submission received! Grade: {grade}")

def update_grades(name, email, student_id, week, grade):
    grades_file = Path("grades/data_submission.csv")
    
    if grades_file.exists():
        df = pd.read_csv(grades_file)
    else:
        # Create new DataFrame if file doesn't exist
        columns = ["Name", "Email", "Student ID"] + \
                 [f"Week {i}" for i in range(1, 16)] + \
                 [f"Quiz {i}" for i in range(1, 11)] + \
                 ["Total"]
        df = pd.DataFrame(columns=columns)
    
    # Update or add new row
    student_mask = (df["Email"] == email) & (df["Student ID"] == student_id)
    
    if student_mask.any():
        df.loc[student_mask, f"Week {week}"] = grade
        df.loc[student_mask, "Total"] = df.loc[student_mask].filter(regex="Week|Quiz").sum(axis=1)
    else:
        new_row = pd.Series(index=df.columns)
        new_row["Name"] = name
        new_row["Email"] = email
        new_row["Student ID"] = student_id
        new_row[f"Week {week}"] = grade
        new_row["Total"] = grade
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Save updated grades
    df.to_csv(grades_file, index=False)

if __name__ == "__main__":
    main()
"""

# Template for quiz#.py pages
def create_quiz_page(quiz_number):
    return f"""
import streamlit as st
import pandas as pd
from pathlib import Path

def main():
    st.title(f"Quiz {quiz_number}")
    
    with st.form(f"quiz_{quiz_number}"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        student_id = st.text_input("Student ID")
        
        # Add quiz questions here
        answer1 = st.text_input("Question 1")
        # Add more questions as needed
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Grade quiz
            grade = grade_quiz(answer1)  # Add more answers as params
            
            # Update grades
            update_grades(name, email, student_id, quiz_number, grade)
            
            st.success(f"Quiz submitted! Grade: {grade}")

def grade_quiz(answer1):  # Add more parameters as needed
    # Implement quiz grading logic
    return 0  # Replace with actual grading

def update_grades(name, email, student_id, quiz, grade):
    grades_file = Path("grades/data_submission.csv")
    
    if grades_file.exists():
        df = pd.read_csv(grades_file)
    else:
        columns = ["Name", "Email", "Student ID"] + \
                 [f"Week {i}" for i in range(1, 16)] + \
                 [f"Quiz {i}" for i in range(1, 11)] + \
                 ["Total"]
        df = pd.DataFrame(columns=columns)
    
    student_mask = (df["Email"] == email) & (df["Student ID"] == student_id)
    
    if student_mask.any():
        df.loc[student_mask, f"Quiz {quiz}"] = grade
        df.loc[student_mask, "Total"] = df.loc[student_mask].filter(regex="Week|Quiz").sum(axis=1)
    else:
        new_row = pd.Series(index=df.columns)
        new_row["Name"] = name
        new_row["Email"] = email
        new_row["Student ID"] = student_id
        new_row[f"Quiz {quiz}"] = grade
        new_row["Total"] = grade
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    df.to_csv(grades_file, index=False)

if __name__ == "__main__":
    main()
"""

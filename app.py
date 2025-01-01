import streamlit as st
import style
from pathlib import Path
import importlib
import pandas as pd

# Configure the Streamlit page
st.set_page_config(
    page_title="ImpactHub",
    page_icon="📚",
    layout="wide"
)

# Apply custom styles
style.apply_styles()

def load_module(module_name):
    """Dynamically import modules for weeks and quizzes"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Error loading module {module_name}: {str(e)}")
        return None

def main():
    # Title with animation (CSS animation applied via style.py)
    st.markdown('<h1 class="animated-title">ImpactHub</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Create tabs for Assignments and Quizzes
    tab_selection = st.sidebar.radio("Select Category:", ["Assignments", "Quizzes"])
    
    if tab_selection == "Assignments":
        st.subheader("Weekly Assignments")
        cols = st.columns(3)  # Create 3 columns for card layout
        
        for week in range(1, 16):
            with cols[week % 3]:
                with st.expander(f"Week {week}", expanded=False):
                    if st.button(f"Open Week {week}", key=f"week_{week}"):
                        module = load_module(f"week{week}")
                        if module:
                            module.run()
                            
                        # Load corresponding grading module
                        grade_module = load_module(f"grade{week}")
                        if grade_module:
                            grade_module.grade()
    
    else:  # Quizzes section
        st.subheader("Quizzes")
        cols = st.columns(2)  # Create 2 columns for quiz layout
        
        for quiz in range(1, 11):
            with cols[quiz % 2]:
                with st.expander(f"Quiz {quiz}", expanded=False):
                    if st.button(f"Open Quiz {quiz}", key=f"quiz_{quiz}"):
                        module = load_module(f"quiz{quiz}")
                        if module:
                            module.run()

    # Initialize grades directory if it doesn't exist
    Path("grades").mkdir(exist_ok=True)
    
    # Initialize submission data file if it doesn't exist
    if not Path("grades/data_submission.csv").exists():
        pd.DataFrame(columns=[
            'student_id', 'assignment_type', 'assignment_number', 
            'submission_date', 'grade', 'feedback'
        ]).to_csv("grades/data_submission.csv", index=False)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from PIL import Image
import os
import sys
from style import apply_style

# Must be the first Streamlit command
st.set_page_config(page_title="ImpactHub", layout="wide")

def load_module(module_path):
    """Dynamically load a Python module"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_flip_card(title, description, key):
    """Create a flip card with hover effect"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(f"📚 {title}", key=f"btn_{key}"):
                try:
                    if "week" in title.lower():
                        module = load_module(f"week{key}.py")
                    else:
                        module = load_module(f"quiz{key}.py")
                    module.main()
                except Exception as e:
                    st.error(f"Error loading module: {str(e)}")
        with col2:
            st.markdown(f"<div class='flip-card-content'>{description}</div>", unsafe_allow_html=True)

def main():
    # Apply custom styling
    apply_style()
    
    # Title with custom styling from style.py
    st.markdown("<div class='moving-title'>ImpactHub</div>", unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Assignments", "Quizzes"])
    
    if page == "Assignments":
        st.header("Weekly Assignments")
        for week in range(1, 16):
            create_flip_card(
                f"Week {week}",
                f"Assignment for Week {week}. Click to view and submit your work.",
                week
            )
            
    else:  # Quizzes page
        st.header("Course Quizzes")
        for quiz in range(1, 11):
            create_flip_card(
                f"Quiz {quiz}",
                f"Quiz {quiz} assessment. Click to start the quiz.",
                quiz
            )
    
    # Initialize or load grades dataframe
    if 'grades_df' not in st.session_state:
        try:
            st.session_state.grades_df = pd.read_csv('grades/data_submission.csv')
        except FileNotFoundError:
            st.session_state.grades_df = pd.DataFrame(columns=[
                'student_id', 'assignment_id', 'submission_date', 'grade'
            ])
            os.makedirs('grades', exist_ok=True)
            st.session_state.grades_df.to_csv('grades/data_submission.csv', index=False)

if __name__ == "__main__":
    main()

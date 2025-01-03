import streamlit as st
import pandas as pd
import os
from style import apply_style
import importlib

# Set page configuration
st.set_page_config(page_title="ImpactHub", layout="wide")

def load_module(module_name):
    """Dynamically import module"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.error(f"Module {module_name} not found!")
        return None

def create_flip_card(title, description, key):
    """Create a flip card with CSS animation"""
    with st.container():
        st.markdown(f"""
            <div class="flip-card" onclick="this.classList.toggle('flipped')" key="{key}">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>{title}</h3>
                    </div>
                    <div class="flip-card-back">
                        <p>{description}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def main():
    # Apply custom styling
    apply_style()
    
    # Title with animation
    st.markdown('<h1 class="moving-title">ImpactHub</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Assignments", "Quizzes"])
    
    if page == "Assignments":
        st.header("Weekly Assignments")
        cols = st.columns(3)
        for week in range(1, 16):
            with cols[week % 3]:
                create_flip_card(
                    f"Week {week}",
                    f"Click to view assignment for Week {week}",
                    f"week_{week}"
                )
                if st.button(f"Open Week {week}", key=f"btn_week_{week}"):
                    module = load_module(f"week{week}")
                    if module:
                        module.main()
    
    else:  # Quizzes page
        st.header("Available Quizzes")
        cols = st.columns(2)
        for quiz in range(1, 11):
            with cols[quiz % 2]:
                create_flip_card(
                    f"Quiz {quiz}",
                    f"Click to start Quiz {quiz}",
                    f"quiz_{quiz}"
                )
                if st.button(f"Start Quiz {quiz}", key=f"btn_quiz_{quiz}"):
                    module = load_module(f"quiz{quiz}")
                    if module:
                        module.main()

    # Initialize or load grades dataframe
    if not os.path.exists("grades"):
        os.makedirs("grades")
    
    try:
        grades_df = pd.read_csv("grades/data_submission.csv")
    except FileNotFoundError:
        grades_df = pd.DataFrame(columns=['student_id', 'assignment', 'submission_date', 'grade'])
        grades_df.to_csv("grades/data_submission.csv", index=False)

if __name__ == "__main__":
    main()

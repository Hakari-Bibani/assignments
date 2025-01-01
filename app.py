import streamlit as st
import base64
from pathlib import Path
import importlib
import pandas as pd
from style import apply_style

def load_module(module_name):
    """Dynamically import a module"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.error(f"Could not load module: {module_name}")
        return None

def create_animated_text():
    """Create animated text using HTML/CSS"""
    st.markdown(
        """
        <style>
        @keyframes slide {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .animated-text {
            color: red;
            font-size: 48px;
            font-weight: bold;
            white-space: nowrap;
            animation: slide 15s linear infinite;
            overflow: hidden;
        }
        </style>
        <div class="animated-text">ImpactHub</div>
        """,
        unsafe_allow_html=True
    )

def main():
    # Apply custom styling
    apply_style()
    
    # Display animated title
    create_animated_text()
    
    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Weeks")
        weeks = [f"Week {i}" for i in range(1, 16)]
        for week in weeks:
            week_num = week.split()[1]
            if st.button(week, key=f"week_{week_num}"):
                week_module = load_module(f"pages.week{week_num}")
                if week_module:
                    st.session_state.current_page = f"week{week_num}"
    
    with col2:
        st.markdown("### Quizzes")
        quizzes = [f"Quiz {i}" for i in range(1, 11)]
        for quiz in quizzes:
            quiz_num = quiz.split()[1]
            if st.button(quiz, key=f"quiz_{quiz_num}"):
                quiz_module = load_module(f"pages.quiz{quiz_num}")
                if quiz_module:
                    st.session_state.current_page = f"quiz{quiz_num}"
    
    # Load current page if set
    if 'current_page' in st.session_state:
        module = load_module(f"pages.{st.session_state.current_page}")
        if module and hasattr(module, 'main'):
            module.main()

if __name__ == "__main__":
    main()

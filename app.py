import streamlit as st
import pandas as pd
import base64
from style import custom_style
import importlib
import sys
from pathlib import Path

# Apply custom styling
custom_style()

def load_module(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.error(f"Could not load module {module_name}")
        return None

def create_animated_title():
    st.markdown("""
        <style>
        @keyframes slide {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .moving-text {
            color: red;
            font-size: 50px;
            font-weight: bold;
            white-space: nowrap;
            animation: slide 15s linear infinite;
            overflow: hidden;
        }
        </style>
        <div class="moving-text">ImpactHub</div>
    """, unsafe_allow_html=True)

def main():
    create_animated_title()
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)

    # Weeks Section
    with col1:
        st.markdown("<h2 style='text-align: center;'>Weekly Assignments</h2>", unsafe_allow_html=True)
        weeks = [f"Week {i}" for i in range(1, 16)]
        for week in weeks:
            week_num = week.split()[1]
            if st.button(week, key=f"week_{week_num}", use_container_width=True):
                module = load_module(f"week{week_num}")
                if module:
                    st.session_state.current_page = f'week{week_num}'

    # Quizzes Section
    with col2:
        st.markdown("<h2 style='text-align: center;'>Quizzes</h2>", unsafe_allow_html=True)
        quizzes = [f"Quiz {i}" for i in range(1, 11)]
        for quiz in quizzes:
            quiz_num = quiz.split()[1]
            if st.button(quiz, key=f"quiz_{quiz_num}", use_container_width=True):
                module = load_module(f"quiz{quiz_num}")
                if module:
                    st.session_state.current_page = f'quiz{quiz_num}'

    # Load the current page
    if st.session_state.current_page != 'home':
        module = load_module(st.session_state.current_page)
        if module and hasattr(module, 'main'):
            module.main()

if __name__ == "__main__":
    main()

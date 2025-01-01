import streamlit as st
from pathlib import Path
import importlib
import pandas as pd
import style
from streamlit_card import card

# Configure page settings
st.set_page_config(page_title="ImpactHub", layout="wide")

# Apply custom styles
style.apply_styles()

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Title with animation
st.markdown("""
    <div class="moving-title">
        <h1>ImpactHub</h1>
    </div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    
    # Weeks tab
    st.header("Weeks")
    for i in range(1, 16):
        if st.button(f"Week {i}", key=f"week_{i}_sidebar"):
            st.session_state.current_page = f'week{i}'
            
    # Quizzes tab
    st.header("Quizzes")
    for i in range(1, 11):
        if st.button(f"Quiz {i}", key=f"quiz_{i}_sidebar"):
            st.session_state.current_page = f'quiz{i}'

# Main content area
if st.session_state.current_page == 'home':
    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Weeks")
        for i in range(1, 16):
            # Create clickable card for each week
            clicked = card(
                title=f"Week {i}",
                text="Click to view assignments and submit work",
                key=f"week_{i}_card"
            )
            if clicked:
                st.session_state.current_page = f'week{i}'
                st.experimental_rerun()
    
    with col2:
        st.header("Quizzes")
        for i in range(1, 11):
            # Create clickable card for each quiz
            clicked = card(
                title=f"Quiz {i}",
                text="Click to take the quiz",
                key=f"quiz_{i}_card"
            )
            if clicked:
                st.session_state.current_page = f'quiz{i}'
                st.experimental_rerun()

else:
    # Dynamic page loading
    try:
        if st.session_state.current_page.startswith('week'):
            week_num = st.session_state.current_page[4:]
            week_module = importlib.import_module(f'pages.week{week_num}')
            week_module.show()
        elif st.session_state.current_page.startswith('quiz'):
            quiz_num = st.session_state.current_page[4:]
            quiz_module = importlib.import_module(f'pages.quiz{quiz_num}')
            quiz_module.show()
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")

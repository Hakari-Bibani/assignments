import streamlit as st
from style import apply_custom_style
import pandas as pd
from pathlib import Path

# Configure Streamlit page
st.set_page_config(page_title="ImpactHub", layout="wide")

# Apply custom styling
apply_custom_style()

# Create title with animation
st.markdown("""
    <div class="moving-title">
        <h1>ImpactHub</h1>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    
    # Assignments section
    st.header("Assignments")
    for week in range(1, 16):
        if st.button(f"Week {week}", key=f"week_{week}"):
            try:
                module = __import__(f"week{week}")
                st.session_state.current_page = f"week{week}"
            except ImportError:
                st.error(f"Week {week} content not available")
    
    # Quizzes section
    st.header("Quizzes")
    for quiz in range(1, 11):
        if st.button(f"Quiz {quiz}", key=f"quiz_{quiz}"):
            try:
                module = __import__(f"quiz{quiz}")
                st.session_state.current_page = f"quiz{quiz}"
            except ImportError:
                st.error(f"Quiz {quiz} content not available")

# Main content area
if st.session_state.current_page == 'main':
    # Create two columns for assignments and quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Weekly Assignments")
        for week in range(1, 16):
            with st.container():
                st.markdown(f"""
                    <div class="card">
                        <h3>Week {week}</h3>
                        <p>Assignment for Week {week}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.header("Quizzes")
        for quiz in range(1, 11):
            with st.container():
                st.markdown(f"""
                    <div class="card">
                        <h3>Quiz {quiz}</h3>
                        <p>Quiz {quiz} Assessment</p>
                    </div>
                """, unsafe_allow_html=True)

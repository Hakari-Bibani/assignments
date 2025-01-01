import streamlit as st
from style import load_css
import json
import pandas as pd

# Load custom CSS
load_css()

# Configure the page
st.set_page_config(page_title="ImpactHub", layout="wide")

# Add custom HTML for animated title
st.markdown("""
    <div class="animated-title">
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
            st.session_state.current_page = f"week{week}"
    
    # Quizzes section
    st.header("Quizzes")
    for quiz in range(1, 11):
        if st.button(f"Quiz {quiz}", key=f"quiz_{quiz}"):
            st.session_state.current_page = f"quiz{quiz}"

# Main content
if st.session_state.current_page == 'main':
    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Assignments")
        for week in range(1, 16):
            with st.container():
                # Create flip card using HTML/CSS
                st.markdown(f"""
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <div class="flip-card-front">
                                <h3>Week {week}</h3>
                            </div>
                            <div class="flip-card-back">
                                <p>Assignment {week} Details</p>
                                <p>Click the Week {week} tab in sidebar to start</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")  # Add spacing between cards
    
    with col2:
        st.header("Quizzes")
        for quiz in range(1, 11):
            with st.container():
                st.markdown(f"""
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <div class="flip-card-front">
                                <h3>Quiz {quiz}</h3>
                            </div>
                            <div class="flip-card-back">
                                <p>Quiz {quiz} Details</p>
                                <p>Click the Quiz {quiz} tab in sidebar to start</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")  # Add spacing between cards

else:
    # Import and run the appropriate week or quiz module
    try:
        module = __import__(st.session_state.current_page)
        module.main()
    except ImportError:
        st.error(f"Module {st.session_state.current_page}.py not found!")

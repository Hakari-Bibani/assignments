import streamlit as st
import style
from pathlib import Path
import base64
import importlib

# Set page configuration
st.set_page_config(page_title="ImpactHub", layout="wide")

def load_css(css_file):
    with open(css_file) as f:
        return st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css("style.py")

# Create animated title
st.markdown("""
    <div class="title-container">
        <h1 class="moving-title">ImpactHub</h1>
    </div>
    """, unsafe_allow_html=True)

# Create two columns for assignments and quizzes
col1, col2 = st.columns(2)

# Assignments section
with col1:
    st.markdown("<h2>Assignments</h2>", unsafe_allow_html=True)
    for week in range(1, 16):
        with st.container():
            st.markdown(f"""
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Week {week}</h3>
                    </div>
                    <div class="flip-card-back">
                        <p>Assignment {week}</p>
                        <button onclick="window.location.href='week{week}.py'">Go to Assignment</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Quizzes section
with col2:
    st.markdown("<h2>Quizzes</h2>", unsafe_allow_html=True)
    for quiz in range(1, 11):
        with st.container():
            st.markdown(f"""
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Quiz {quiz}</h3>
                    </div>
                    <div class="flip-card-back">
                        <p>Quiz {quiz}</p>
                        <button onclick="window.location.href='quiz{quiz}.py'">Go to Quiz</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")

# Assignment tabs in sidebar
st.sidebar.markdown("### Assignments")
for week in range(1, 16):
    if st.sidebar.button(f"Week {week}"):
        # Import and run the corresponding week's script
        week_module = importlib.import_module(f"week{week}")
        week_module.main()

# Quiz tabs in sidebar
st.sidebar.markdown("### Quizzes")
for quiz in range(1, 11):
    if st.sidebar.button(f"Quiz {quiz}"):
        # Import and run the corresponding quiz script
        quiz_module = importlib.import_module(f"quiz{quiz}")
        quiz_module.main()

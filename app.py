import streamlit as st
from style import apply_custom_style
import importlib
import os

# Page configuration
st.set_page_config(
    page_title="ImpactHub",
    page_icon="🎓",
    layout="wide"
)

# Apply custom styling
st.markdown(apply_custom_style(), unsafe_allow_html=True)

# Main title with animation
st.markdown('<h1 class="main-title">ImpactHub</h1>', unsafe_allow_html=True)

def create_card(title, module_name):
    with st.container():
        st.markdown(f'''
        <div class="card">
            <h3>{title}</h3>
        </div>
        ''', unsafe_allow_html=True)
        if st.button(f"Start", key=f"start_{module_name}"):
            try:
                module = importlib.import_module(module_name)
                return module
            except ImportError:
                st.error(f"Could not load module {module_name}")
                return None

# Create two columns for Weeks and Quizzes
col1, col2 = st.columns(2)

# Weeks section
with col1:
    st.markdown('<h2 class="section-title">Weekly Assignments</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    for week in range(1, 16):
        create_card(f"Week {week}", f"week{week}")
    st.markdown('</div>', unsafe_allow_html=True)

# Quizzes section
with col2:
    st.markdown('<h2 class="section-title">Quizzes</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    for quiz in range(1, 11):
        create_card(f"Quiz {quiz}", f"quiz{quiz}")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; background-color: #f0f2f6;">
    <p>© 2025 ImpactHub. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from pathlib import Path
import importlib
import sys
from style import apply_style

# Configure page settings
st.set_page_config(
    page_title="ImpactHub",
    page_icon="📚",
    layout="wide"
)

# Apply custom styling
apply_style()

# Create animated title
st.markdown("""
    <div class="animate-title">
        <h1>ImpactHub</h1>
    </div>
""", unsafe_allow_html=True)

def load_module(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.error(f"Could not load module: {module_name}")
        return None

def main():
    # Create two columns for weeks and quizzes
    col1, col2 = st.columns(2)
    
    # Weeks column
    with col1:
        st.markdown("### 📝 Weekly Assignments")
        for week in range(1, 16):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>Week {week}</h3>
                    <p>Assignment {week}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Start Week {week}", key=f"week_{week}"):
                    module = load_module(f"week{week}")
                    if module:
                        module.run()
    
    # Quizzes column
    with col2:
        st.markdown("### 📊 Quizzes")
        for quiz in range(1, 11):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>Quiz {quiz}</h3>
                    <p>Assessment {quiz}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Start Quiz {quiz}", key=f"quiz_{quiz}"):
                    module = load_module(f"quiz{quiz}")
                    if module:
                        module.run()

if __name__ == "__main__":
    main()

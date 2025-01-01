import streamlit as st
from style import apply_custom_style
import importlib
import sys
import os

def load_module(module_name):
    """Dynamically import a module"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.error(f"Could not load module: {module_name}")
        return None

def main():
    # Apply custom styling
    apply_custom_style()
    
    # Title with animation
    st.markdown(
        """
        <div class="animated-title">
            <h1>ImpactHub</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## Assignments")
        for week in range(1, 16):
            if st.button(f"Week {week}", key=f"week_{week}"):
                module_name = f"week{week}"
                module = load_module(module_name)
                if module and hasattr(module, 'main'):
                    module.main()
    
    with col2:
        st.markdown("## Quizzes")
        for quiz in range(1, 11):
            if st.button(f"Quiz {quiz}", key=f"quiz_{quiz}"):
                module_name = f"quiz{quiz}"
                module = load_module(module_name)
                if module and hasattr(module, 'main'):
                    module.main()

if __name__ == "__main__":
    main()

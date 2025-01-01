import streamlit as st
import style
from pathlib import Path
import importlib
import sys

# Configure page settings
st.set_page_config(page_title="ImpactHub", layout="wide")

def main():
    # Apply custom styles
    style.apply_styles()
    
    # Animated title with custom CSS
    st.markdown("""
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
    """, unsafe_allow_html=True)

    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)

    # Weeks Section
    with col1:
        st.markdown("## Weeks")
        for week_num in range(1, 16):
            if st.button(f"Week {week_num}", key=f"week_{week_num}", 
                        use_container_width=True):
                try:
                    # Import and run the corresponding week module
                    week_module = importlib.import_module(f"week{week_num}")
                    week_module.main()
                except ImportError:
                    st.error(f"Week {week_num} content not found!")

    # Quizzes Section
    with col2:
        st.markdown("## Quizzes")
        for quiz_num in range(1, 11):
            if st.button(f"Quiz {quiz_num}", key=f"quiz_{quiz_num}", 
                        use_container_width=True):
                try:
                    # Import and run the corresponding quiz module
                    quiz_module = importlib.import_module(f"quiz{quiz_num}")
                    quiz_module.main()
                except ImportError:
                    st.error(f"Quiz {quiz_num} content not found!")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from pathlib import Path
import importlib
import sys

# Configure page settings
st.set_page_config(page_title="ImpactHub", layout="wide")

# Import custom style
import style

def main():
    # Apply custom styles for the moving title
    st.markdown(
        """
        <style>
        @keyframes moveText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .moving-text {
            color: red;
            font-size: 48px;
            font-weight: bold;
            white-space: nowrap;
            animation: moveText 15s linear infinite;
            overflow: hidden;
        }
        </style>
        <div class="moving-text">Welcome to ImpactHub</div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)  # Add some spacing
    
    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)
    
    # Weekly Assignments Section
    with col1:
        st.markdown("### Weekly Assignments")
        for week in range(1, 16):
            if st.button(f"Week {week}", key=f"week_{week}", 
                        use_container_width=True,
                        **style.button_style):
                # Import and run the corresponding week's script
                try:
                    week_module = importlib.import_module(f'pages.week{week}')
                    st.session_state.current_page = f'week{week}'
                    st.experimental_rerun()
                except ImportError as e:
                    st.error(f"Error loading Week {week}: {str(e)}")
    
    # Quizzes Section
    with col2:
        st.markdown("### Quizzes")
        for quiz in range(1, 11):
            if st.button(f"Quiz {quiz}", key=f"quiz_{quiz}", 
                        use_container_width=True,
                        **style.button_style):
                # Import and run the corresponding quiz script
                try:
                    quiz_module = importlib.import_module(f'pages.quiz{quiz}')
                    st.session_state.current_page = f'quiz{quiz}'
                    st.experimental_rerun()
                except ImportError as e:
                    st.error(f"Error loading Quiz {quiz}: {str(e)}")

if __name__ == "__main__":
    main()

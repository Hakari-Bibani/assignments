import streamlit as st
from style import apply_custom_style
import importlib
import sys
import os

# Apply custom styling
apply_custom_style()

def main():
    # Set page config
    st.set_page_config(
        page_title="ImpactHub",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom title with animation
    st.markdown(
        """
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)

    with col1:
        st.header("Assignments")
        for week in range(1, 16):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>Week {week}</h3>
                    <p>Assignment for Week {week}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start Week {week}", key=f"week_{week}"):
                    try:
                        # Dynamically import week module
                        week_module = importlib.import_module(f"week{week}")
                        week_module.run()
                    except ImportError:
                        st.error(f"Week {week} content not found.")

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
                
                if st.button(f"Start Quiz {quiz}", key=f"quiz_{quiz}"):
                    try:
                        # Dynamically import quiz module
                        quiz_module = importlib.import_module(f"quiz{quiz}")
                        quiz_module.run()
                    except ImportError:
                        st.error(f"Quiz {quiz} content not found.")

if __name__ == "__main__":
    main()

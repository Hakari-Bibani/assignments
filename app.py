import streamlit as st
from style import apply_custom_style
import pandas as pd
import os

def main():
    # Apply custom styling
    apply_custom_style()
    
    # Title with animation effect using HTML/CSS
    st.markdown(
        """
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Create tabs for Assignments and Quizzes
    tab_selection = st.sidebar.radio("Select Category:", ["Assignments", "Quizzes"])
    
    if tab_selection == "Assignments":
        st.header("Weekly Assignments")
        # Create columns for a grid layout
        cols = st.columns(3)
        for i in range(15):
            with cols[i % 3]:
                if st.button(f"Week {i+1}", key=f"week_{i+1}", 
                           use_container_width=True):
                    try:
                        # Import and run the corresponding week's script
                        week_module = __import__(f"week{i+1}")
                        week_module.run()
                    except ImportError:
                        st.error(f"Week {i+1} content not found.")
    
    else:  # Quizzes tab
        st.header("Quizzes")
        # Create columns for a grid layout
        cols = st.columns(3)
        for i in range(10):
            with cols[i % 3]:
                if st.button(f"Quiz {i+1}", key=f"quiz_{i+1}", 
                           use_container_width=True):
                    try:
                        # Import and run the corresponding quiz script
                        quiz_module = __import__(f"quiz{i+1}")
                        quiz_module.run()
                    except ImportError:
                        st.error(f"Quiz {i+1} content not found.")

    # Load and display grades if they exist
    try:
        grades_df = pd.read_csv('grades/data_submission.csv')
        if not grades_df.empty:
            st.sidebar.markdown("---")
            st.sidebar.header("Grades Overview")
            st.sidebar.dataframe(grades_df)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()

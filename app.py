import streamlit as st
import pandas as pd
from style import set_page_style, create_card
import importlib

def load_module(module_name):
    """Dynamically import modules for weeks and quizzes"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Error loading module {module_name}: {str(e)}")
        return None

def main():
    # Set page configuration
    st.set_page_config(
        page_title="ImpactHub",
        page_icon="📚",
        layout="wide"
    )
    
    # Apply custom styling
    set_page_style()
    
    # Display animated title
    st.markdown('<h1 class="main-title">ImpactHub</h1>', unsafe_allow_html=True)
    
    # Create two columns for weeks and quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="list-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="list-title">Weekly Assignments</h2>', unsafe_allow_html=True)
        
        # Generate cards for weeks 1-15
        for week in range(1, 16):
            with st.expander(f"Week {week}"):
                st.markdown(create_card(
                    f"Week {week} Assignment",
                    f"Complete the assignments for Week {week}"
                ), unsafe_allow_html=True)
                
                if st.button(f"Start Week {week}", key=f"week_{week}"):
                    week_module = load_module(f"week{week}")
                    if week_module:
                        week_module.run()
                        # After completion, run grading
                        grade_module = load_module(f"grade{week}")
                        if grade_module:
                            grade_module.grade()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="list-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="list-title">Quizzes</h2>', unsafe_allow_html=True)
        
        # Generate cards for quizzes 1-10
        for quiz in range(1, 11):
            with st.expander(f"Quiz {quiz}"):
                st.markdown(create_card(
                    f"Quiz {quiz}",
                    f"Take Quiz {quiz}"
                ), unsafe_allow_html=True)
                
                if st.button(f"Start Quiz {quiz}", key=f"quiz_{quiz}"):
                    quiz_module = load_module(f"quiz{quiz}")
                    if quiz_module:
                        quiz_module.run()
                        # After completion, run grading
                        grade_module = load_module(f"grade{quiz}")
                        if grade_module:
                            grade_module.grade()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Add footer with submission data
    st.markdown("---")
    try:
        submissions_df = pd.read_csv('grades/data_submission.csv')
        st.write("Recent Submissions:")
        st.dataframe(submissions_df.tail())
    except Exception as e:
        st.warning("No submission data available yet.")

if __name__ == "__main__":
    main()

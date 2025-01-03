import streamlit as st
from style import apply_style
import importlib
import os

# Set page configuration
st.set_page_config(page_title="ImpactHub", layout="wide")

def load_module(module_name):
    """Dynamically import week or quiz modules"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        st.error(f"Module {module_name} not found!")
        return None

def main():
    # Apply custom styling
    apply_style()
    
    # Create animated title using HTML and CSS
    st.markdown(
        """
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create sidebar navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Select Section:", ["Assignments", "Quizzes"])

    if section == "Assignments":
        weeks = [f"Week {i}" for i in range(1, 16)]
        selected_week = st.sidebar.selectbox("Select Week:", weeks)
        
        if selected_week:
            week_num = int(selected_week.split()[1])
            module = load_module(f"week{week_num}")
            if module:
                module.main()  # Execute the week's main function

    else:  # Quizzes section
        quizzes = [f"Quiz {i}" for i in range(1, 11)]
        selected_quiz = st.sidebar.selectbox("Select Quiz:", quizzes)
        
        if selected_quiz:
            quiz_num = int(selected_quiz.split()[1])
            module = load_module(f"quiz{quiz_num}")
            if module:
                module.main()  # Execute the quiz's main function

    # Main content area with flip cards (shown when no specific week/quiz is selected)
    if not st.session_state.get('module_selected', False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Assignments")
            for i in range(1, 16):
                with st.container():
                    st.markdown(
                        f"""
                        <div class="flip-card">
                            <div class="flip-card-inner">
                                <div class="flip-card-front">
                                    <h3>Week {i}</h3>
                                </div>
                                <div class="flip-card-back">
                                    <p>Assignment for Week {i}</p>
                                    <p>Click to view details</p>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
        with col2:
            st.markdown("### Quizzes")
            for i in range(1, 11):
                with st.container():
                    st.markdown(
                        f"""
                        <div class="flip-card">
                            <div class="flip-card-inner">
                                <div class="flip-card-front">
                                    <h3>Quiz {i}</h3>
                                </div>
                                <div class="flip-card-back">
                                    <p>Quiz {i} Details</p>
                                    <p>Click to start</p>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()

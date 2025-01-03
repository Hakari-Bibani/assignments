import streamlit as st
from style import apply_style
import base64

# Apply custom styling
apply_style()

def create_flip_card(title, content):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(
                f"""
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <h3>{title}</h3>
                        </div>
                        <div class="flip-card-back">
                            <p>{content}</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def add_animated_text():
    st.markdown(
        """
        <div class="animated-title">
            <h1>ImpactHub</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    # Add animated title
    add_animated_text()
    
    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)
    
    # Assignments section
    with col1:
        st.markdown("## Assignments")
        assignments = [f"Assignment {i}" for i in range(1, 16)]
        for assignment in assignments:
            create_flip_card(assignment, f"Click to view {assignment} details")
    
    # Quizzes section
    with col2:
        st.markdown("## Quizzes")
        quizzes = [f"Quiz {i}" for i in range(1, 11)]
        for quiz in quizzes:
            create_flip_card(quiz, f"Click to view {quiz} details")

    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        st.markdown("### Assignments")
        for i in range(1, 16):
            st.button(f"Assignment {i}")
        
        st.markdown("### Quizzes")
        for i in range(1, 11):
            st.button(f"Quiz {i}")

if __name__ == "__main__":
    main()

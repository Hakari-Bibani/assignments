import streamlit as st
import streamlit.components.v1 as components
from style import apply_style, get_flip_card_html

def main():
    # Apply custom styling
    apply_style()
    
    # Title with animation
    st.markdown("""
        <div class="animated-title">
            <h1>ImpactHub</h1>
        </div>
    """, unsafe_allow_html=True)

    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2>Assignments</h2>", unsafe_allow_html=True)
        weeks = [f"Week {i}" for i in range(1, 16)]
        week_content = [f"Assignment {i}" for i in range(1, 16)]
        
        # Generate flip cards for weeks
        for week, content in zip(weeks, week_content):
            flip_card = get_flip_card_html(week, content, f"week{week.split()[-1]}.py")
            components.html(flip_card, height=200)

    with col2:
        st.markdown("<h2>Quizzes</h2>", unsafe_allow_html=True)
        quizzes = [f"Quiz {i}" for i in range(1, 11)]
        quiz_content = [f"Quiz {i} Content" for i in range(1, 11)]
        
        # Generate flip cards for quizzes
        for quiz, content in zip(quizzes, quiz_content):
            flip_card = get_flip_card_html(quiz, content, f"quiz{quiz.split()[-1]}.py")
            components.html(flip_card, height=200)

if __name__ == "__main__":
    main()

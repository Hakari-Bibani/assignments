import streamlit as st
from style import apply_custom_style
import time

def main():
    # Apply custom styling
    apply_custom_style()
    
    # Create animated title
    st.markdown(
        """
        <div class="moving-title">
            <h1 class="red-title">ImpactHub</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create two columns for weeks and quizzes
    col1, col2 = st.columns(2)

    # Weeks section
    with col1:
        st.markdown("<h2>Weeks</h2>", unsafe_allow_html=True)
        for week in range(1, 16):
            st.link_button(f"Week {week}", f"Week_{week}")

    # Quizzes section
    with col2:
        st.markdown("<h2>Quizzes</h2>", unsafe_allow_html=True)
        for quiz in range(1, 11):
            st.link_button(f"Quiz {quiz}", f"Quiz_{quiz}")

if __name__ == "__main__":
    main()

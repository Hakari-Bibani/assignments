import streamlit as st
import base64
import os
from style import page_config

def create_animation_html(text):
    return f"""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <h1 style="color: red; font-size: 3.5em;">
            <marquee behavior="alternate" direction="left">{text}</marquee>
        </h1>
    </div>
    """

def main():
    page_config()
    
    # Display animated title
    st.markdown(create_animation_html("ImpactHub"), unsafe_allow_html=True)
    
    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)
    
    # Weeks Section
    with col1:
        st.markdown("<h2 style='text-align: center;'>Weeks</h2>", unsafe_allow_html=True)
        for week in range(1, 16):
            if st.button(f"Week {week}", key=f"week_{week}", 
                        use_container_width=True,
                        help=f"Click to go to Week {week} assignments"):
                try:
                    # Import and run the specific week's script
                    exec(f"import week{week}")
                    exec(f"week{week}.main()")
                except ImportError:
                    st.error(f"Week {week} content is not available yet.")
    
    # Quizzes Section
    with col2:
        st.markdown("<h2 style='text-align: center;'>Quizzes</h2>", unsafe_allow_html=True)
        for quiz in range(1, 11):
            if st.button(f"Quiz {quiz}", key=f"quiz_{quiz}", 
                        use_container_width=True,
                        help=f"Click to go to Quiz {quiz}"):
                try:
                    # Import and run the specific quiz script
                    exec(f"import quiz{quiz}")
                    exec(f"quiz{quiz}.main()")
                except ImportError:
                    st.error(f"Quiz {quiz} content is not available yet.")

if __name__ == "__main__":
    main()

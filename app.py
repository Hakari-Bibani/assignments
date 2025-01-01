import streamlit as st
import webbrowser
import style
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="ImpactHub",
    page_icon="🎓",
    layout="wide"
)

def main():
    # Apply custom styles
    style.apply_custom_styles()
    
    # Create animated title
    st.markdown("""
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
    """, unsafe_allow_html=True)

    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)

    # Weeks Section
    with col1:
        st.markdown("<h2 style='text-align: center;'>Weekly Assignments</h2>", unsafe_allow_html=True)
        for week in range(1, 16):
            # Create flip card for each week
            st.markdown(f"""
                <div class="flip-card" onclick="window.location.href='week{week}.py'">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <h3>Week {week}</h3>
                        </div>
                        <div class="flip-card-back">
                            <p>Click to view Week {week} assignments</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Quizzes Section
    with col2:
        st.markdown("<h2 style='text-align: center;'>Quizzes</h2>", unsafe_allow_html=True)
        for quiz in range(1, 11):
            # Create flip card for each quiz
            st.markdown(f"""
                <div class="flip-card" onclick="window.location.href='quiz{quiz}.py'">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <h3>Quiz {quiz}</h3>
                        </div>
                        <div class="flip-card-back">
                            <p>Click to view Quiz {quiz}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

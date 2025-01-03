import streamlit as st
import style
from PIL import Image

def main():
    # Apply custom styling
    style.apply_styles()
    
    # Animated title
    st.markdown(
        """
        <div class="animate-title">
            <h1>ImpactHub</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Assignments")
        for i in range(1, 16):
            with st.container():
                st.markdown(f"""
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <div class="flip-card-front">
                                <h3>Assignment {i}</h3>
                            </div>
                            <div class="flip-card-back">
                                <p>Click to view Assignment {i}</p>
                                <a href="/as{i}" target="_self">Go to Assignment</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.header("Quizzes")
        for i in range(1, 11):
            with st.container():
                st.markdown(f"""
                    <div class="flip-card">
                        <div class="flip-card-inner">
                            <div class="flip-card-front">
                                <h3>Quiz {i}</h3>
                            </div>
                            <div class="flip-card-back">
                                <p>Click to view Quiz {i}</p>
                                <a href="/quiz{i}" target="_self">Go to Quiz</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

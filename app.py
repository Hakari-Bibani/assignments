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

# style.py
import streamlit as st

def apply_custom_style():
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Moving title animation */
        @keyframes moveTitle {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }
        
        .red-title {
            display: inline-block;
            color: red;
            font-size: 3.5rem;
            font-weight: bold;
            animation: moveTitle 15s linear infinite;
        }
        
        /* Card styling */
        .stButton > button {
            width: 100%;
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            background-color: #f8f9fa;
        }
        
        h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }
        </style>
    """, unsafe_allow_html=True)

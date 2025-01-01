
import streamlit as st
import pandas as pd
from pathlib import Path
import importlib
import sys
from style import apply_style
import base64

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

def load_module(module_name):
    """Dynamically import module"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Error loading module {module_name}: {e}")
        return None

def create_animated_title():
    st.markdown("""
        <style>
        @keyframes slideRight {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(0); }
        }
        .sliding-header {
            animation: slideRight 2s ease-out;
            font-size: 3em;
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
            padding: 20px;
        }
        </style>
        <div class="sliding-header">ImpactHub</div>
    """, unsafe_allow_html=True)

def create_flip_card(title, onClick):
    return f"""
        <div class="flip-card" onclick="{onClick}">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <h3>{title}</h3>
                </div>
                <div class="flip-card-back">
                    <p>Click to view {title}</p>
                </div>
            </div>
        </div>
    """

def main():
    # Apply custom styling
    apply_style()
    
    # Create animated title
    create_animated_title()

    if st.session_state.current_page == 'main':
        # Create two columns for Assignments and Quizzes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h2 style='text-align: center;'>Assignments</h2>", unsafe_allow_html=True)
            for week in range(1, 16):
                card_html = create_flip_card(f"Week {week}", f"Streamlit.setComponentValue('current_page', 'week{week}')")
                st.markdown(card_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h2 style='text-align: center;'>Quizzes</h2>", unsafe_allow_html=True)
            for quiz in range(1, 11):
                card_html = create_flip_card(f"Quiz {quiz}", f"Streamlit.setComponentValue('current_page', 'quiz{quiz}')")
                st.markdown(card_html, unsafe_allow_html=True)
    
    else:
        # Load and display the appropriate module
        module_name = st.session_state.current_page
        module = load_module(module_name)
        if module:
            module.main()
        
        if st.button("Back to Main Page"):
            st.session_state.current_page = 'main'
            st.experimental_rerun()

if __name__ == "__main__":
    main()

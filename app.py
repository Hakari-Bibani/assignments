import streamlit as st
import importlib
import os
from style import apply_styles

def load_page(page_name):
    """Dynamically import and run the specified page module"""
    try:
        module = importlib.import_module(page_name)
        module.main()
    except ImportError:
        st.error(f"Error: Could not load {page_name}")

def create_flip_card(title, description, page_name):
    """Create a flip card with navigation"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            # Card front
            with st.expander(title, expanded=True):
                st.write(description)
                
                # Navigation button
                if st.button(f"Go to {title}", key=f"btn_{page_name}"):
                    st.session_state.current_page = page_name
                    st.experimental_rerun()

def main():
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'

    # Apply custom styles
    apply_styles()

    if st.session_state.current_page == 'main':
        st.title("ImpactHub")
        
        # Create two columns for Assignments and Quizzes
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Assignments")
            for i in range(1, 16):
                create_flip_card(
                    f"Assignment {i}",
                    f"Click to view and complete Assignment {i}",
                    f"as{i}"
                )
        
        with col2:
            st.subheader("Quizzes")
            for i in range(1, 11):
                create_flip_card(
                    f"Quiz {i}",
                    f"Click to attempt Quiz {i}",
                    f"quiz{i}"
                )
    else:
        # Load the selected page
        load_page(st.session_state.current_page)
        
        # Add back button
        if st.button("Back to Main Page"):
            st.session_state.current_page = 'main'
            st.experimental_rerun()

if __name__ == "__main__":
    main()

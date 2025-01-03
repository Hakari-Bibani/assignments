import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Page configuration
st.set_page_config(page_title="ImpactHub", layout="wide")

# Header with animated title
st.markdown("""
    <h1 style="color: red; font-size: 3em; animation: fadeIn 2s infinite;">ImpactHub</h1>
    <style>
        @keyframes fadeIn {
            0% {opacity: 0;}
            50% {opacity: 1;}
            100% {opacity: 0;}
        }
    </style>
""", unsafe_allow_html=True)

# Main page layout
st.header("Assignments and Quizzes")

# Flip cards for Assignments
st.subheader("Assignments")
for i in range(1, 16):
    with st.expander(f"Assignment {i}"):
        if st.button(f"Go to Assignment {i}"):
            switch_page(f"as{i}")

# Flip cards for Quizzes
st.subheader("Quizzes")
for i in range(1, 11):
    with st.expander(f"Quiz {i}"):
        if st.button(f"Go to Quiz {i}"):
            switch_page(f"quiz{i}")

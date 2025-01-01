import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        .main { background-color: #f0f0f0; }
        </style>
        """,
        unsafe_allow_html=True
    )

import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    .big-red-text {
        color: red;
        font-size: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

import streamlit as st

def apply_card_style():
    st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

def set_page_theme():
    st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

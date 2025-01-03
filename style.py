import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        body {
            font-family: 'Tiranti Solid Std Regular', sans-serif;
        }
        h1 {
            text-align: center;
            font-size: 3rem;
            color: red;
        }
        .st-expander {
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .st-button {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

apply_styles()

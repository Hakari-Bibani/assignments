# style.py
import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .big-font {
            font-size:50px !important;
            color: red;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)

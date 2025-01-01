# style.py
import streamlit as st

def apply_style():
    # Custom CSS
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 2rem;
        }
        
        /* Headers */
        .css-10trblm {
            color: #1a237e;
            margin-bottom: 1rem;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #1a237e;
            color: white;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #283593;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Text inputs */
        .stTextInput > div > div > input {
            border-radius: 4px;
            border: 1px solid #e0e0e0;
        }
        
        /* Text areas */
        .stTextArea > div > div > textarea {
            border-radius: 4px;
            border: 1px solid #e0e0e0;
        }
        
        /* Success messages */
        .success {
            padding: 1rem;
            border-radius: 4px;
            background-color: #c8e6c9;
            color: #2e7d32;
        }
        
        /* Error messages */
        .error {
            padding: 1rem;
            border-radius: 4px;
            background-color: #ffcdd2;
            color: #c62828;
        }
        </style>
    """, unsafe_allow_html=True)

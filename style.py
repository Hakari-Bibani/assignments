import streamlit as st

def apply_custom_style():
    # Custom CSS styling
    st.markdown("""
        <style>
        /* Moving title animation */
        @keyframes moveText {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }
        
        .moving-title h1 {
            display: inline-block;
            animation: moveText 15s linear infinite;
            color: red;
            font-size: 3.5rem;
            font-weight: bold;
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            margin: 0.5rem 0;
            padding: 0.5rem;
            border-radius: 5px;
            background-color: #f0f2f6;
            transition: background-color 0.3s;
        }
        
        .stButton button:hover {
            background-color: #e0e2e6;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        
        /* Headers styling */
        h1, h2, h3 {
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

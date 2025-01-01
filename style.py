import streamlit as st

def apply_styles():
    # Custom CSS styles
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
            font-size: 4rem;
            font-weight: bold;
        }
        
        /* Button styles */
        .stButton > button {
            width: 100%;
            margin: 0.5rem 0;
            background-color: #f0f2f6;
            border: 1px solid #e0e3e9;
            border-radius: 5px;
            padding: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #e0e3e9;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Section headers */
        h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

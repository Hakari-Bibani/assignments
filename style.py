import streamlit as st

def apply_custom_style():
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Moving title animation */
        @keyframes moveTitle {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }
        
        .red-title {
            display: inline-block;
            color: red;
            font-size: 3.5rem;
            font-weight: bold;
            animation: moveTitle 15s linear infinite;
        }
        
        /* Card styling */
        .stButton > button {
            width: 100%;
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            background-color: #f8f9fa;
        }
        
        h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }
        </style>
    """, unsafe_allow_html=True)

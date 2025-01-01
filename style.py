import streamlit as st

def apply_style():
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Animated title */
        @keyframes moveTitle {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(10%); }
            100% { transform: translateX(-100%); }
        }
        
        .animate-title {
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }
        
        .animate-title h1 {
            color: #FF0000;
            font-size: 3.5rem;
            animation: moveTitle 10s linear infinite;
            display: inline-block;
        }
        
        /* Card styling */
        .card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        .card h3 {
            color: #1E88E5;
            margin: 0 0 0.5rem 0;
        }
        
        .card p {
            color: #666;
            margin: 0;
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            border-radius: 5px;
            margin-top: 0.5rem;
            background-color: #1E88E5;
            color: white;
        }
        
        .stButton button:hover {
            background-color: #1565C0;
        }
        </style>
    """, unsafe_allow_html=True)

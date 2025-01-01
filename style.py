import streamlit as st

def apply_custom_style():
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Main title styling */
        .moving-title {
            text-align: center;
            animation: moveTitle 2s infinite;
        }
        
        .moving-title h1 {
            color: #FF0000;
            font-size: 4rem;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        @keyframes moveTitle {
            0% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
        }
        
        /* Card styling */
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #1E1E1E;
            margin-bottom: 10px;
        }
        
        .card p {
            color: #666;
            font-size: 0.9rem;
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #45a049;
        }
        
        /* Header styling */
        .css-1v0mbdj.etr89bj1 h2 {
            color: #2C3E50;
            font-size: 1.8rem;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

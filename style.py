import streamlit as st

def apply_style():
    """Apply custom styling to the application"""
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes moveText {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(20%); }
            100% { transform: translateX(-100%); }
        }
        
        .moving-title {
            color: red;
            font-size: 4em;
            font-weight: bold;
            animation: moveText 10s linear infinite;
            white-space: nowrap;
            margin-bottom: 2em;
        }
        
        /* Flip card styling */
        .flip-card {
            background-color: transparent;
            width: 100%;
            height: 200px;
            perspective: 1000px;
            margin-bottom: 20px;
            cursor: pointer;
        }
        
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
            transform-style: preserve-3d;
        }
        
        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }
        
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            padding: 20px;
        }
        
        .flip-card-front {
            background: linear-gradient(145deg, #2e7d32, #1b5e20);
            color: white;
        }
        
        .flip-card-back {
            background: linear-gradient(145deg, #1976d2, #1565c0);
            color: white;
            transform: rotateY(180deg);
        }
        
        /* Custom button styling */
        .stButton button {
            width: 100%;
            margin-top: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        
        .stButton button:hover {
            background-color: #45a049;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f5f5f5;
        }
        
        /* Headers styling */
        h1, h2, h3 {
            font-family: 'Arial', sans-serif;
            margin-bottom: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

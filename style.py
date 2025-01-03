import streamlit as st

def apply_style():
    """Apply custom styling to the Streamlit app"""
    
    # Custom CSS for the entire application
    st.markdown("""
        <style>
        /* Moving title animation */
        @keyframes moveText {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            font-size: 4em;
            color: red;
            font-weight: bold;
            text-align: center;
            animation: moveText 10s linear infinite;
            white-space: nowrap;
            overflow: hidden;
            margin: 20px 0;
        }
        
        /* Flip card styling */
        .flip-card {
            background-color: transparent;
            perspective: 1000px;
            margin: 10px 0;
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
            padding: 20px;
            border-radius: 10px;
        }
        
        .flip-card-front {
            background-color: #f0f2f6;
            color: #31333F;
        }
        
        .flip-card-back {
            background-color: #31333F;
            color: white;
            transform: rotateY(180deg);
        }
        
        .flip-card-content {
            padding: 10px;
            background-color: #f0f2f6;
            border-radius: 5px;
            margin: 5px 0;
            transition: all 0.3s ease;
        }
        
        .flip-card-content:hover {
            background-color: #e0e2e6;
            transform: scale(1.02);
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        
        /* Header styling */
        h1, h2, h3 {
            color: #31333F;
            margin: 20px 0;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        </style>
    """, unsafe_allow_html=True)

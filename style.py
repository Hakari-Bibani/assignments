import streamlit as st

def apply_style():
    """Apply custom styling to the Streamlit app"""
    
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
        
        .moving-title h1 {
            display: inline-block;
            animation: moveTitle 15s linear infinite;
            color: #FF0000;
            font-size: 3.5rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        /* Flip Card Styling */
        .flip-card {
            background-color: transparent;
            width: 300px;
            height: 200px;
            perspective: 1000px;
            margin: 1rem 0;
        }

        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
            transform-style: preserve-3d;
            cursor: pointer;
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
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .flip-card-front {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
        }

        .flip-card-back {
            background: linear-gradient(45deg, #2a5298, #1e3c72);
            color: white;
            transform: rotateY(180deg);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f0f2f6;
        }
        
        /* Improve sidebar selections */
        .stSelectbox {
            background-color: white;
            border-radius: 5px;
            margin: 0.5rem 0;
        }
        
        /* General text improvements */
        h1, h2, h3 {
            font-family: 'Arial', sans-serif;
            margin-bottom: 1rem;
        }
        
        p {
            font-size: 1rem;
            line-height: 1.5;
        }
        </style>
    """, unsafe_allow_html=True)

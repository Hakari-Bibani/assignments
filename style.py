import streamlit as st

def apply_style():
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
            color: red;
            font-size: 3.5rem;
            font-weight: bold;
            animation: moveTitle 15s linear infinite;
        }
        
        /* Flip Card Styling */
        .flip-card {
            background-color: transparent;
            width: 100%;
            height: 120px;
            perspective: 1000px;
            margin-bottom: 1rem;
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
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            padding: 1rem;
        }

        .flip-card-front {
            background: linear-gradient(45deg, #1e88e5, #1565c0);
            color: white;
        }

        .flip-card-back {
            background: linear-gradient(45deg, #43a047, #2e7d32);
            color: white;
            transform: rotateY(180deg);
        }

        /* Button Styling */
        .stButton button {
            width: 100%;
            background-color: #1565c0;
            color: white;
            border: none;
            padding: 0.5rem;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .stButton button:hover {
            background-color: #0d47a1;
        }

        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 4rem;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 4px;
            color: #0d47a1;
            font-weight: bold;
        }

        .stTabs [aria-selected="true"] {
            background-color: #1565c0;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
